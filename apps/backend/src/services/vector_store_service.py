"""LlamaIndex + Pinecone vector store service for ingestion and retrieval."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from llama_index.core import Document

from core.config import Config

logger = logging.getLogger(__name__)


def _get_pinecone_index():
    """Lazily create Pinecone index client."""
    try:
        from pinecone import Pinecone

        pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        return pc.Index(Config.PINECONE_INDEX_NAME)
    except ImportError as e:
        raise RuntimeError("Pinecone package not installed. Run: pip install pinecone") from e
    except Exception as e:
        logger.error("Failed to connect to Pinecone: %s", e)
        raise


def _get_vector_store():
    """Create LlamaIndex PineconeVectorStore."""
    from llama_index.vector_stores.pinecone import PineconeVectorStore

    pinecone_index = _get_pinecone_index()
    return PineconeVectorStore(
        pinecone_index=pinecone_index,
        namespace=Config.PINECONE_NAMESPACE or None,
    )


def _get_embed_model():
    """Create OpenAI embedding model."""
    from llama_index.embeddings.openai import OpenAIEmbedding

    return OpenAIEmbedding(
        model=Config.EMBEDDING_MODEL,
        api_key=Config.OPENAI_API_KEY,
    )


def _load_document(path: Path) -> Document | None:
    """Load a single file into a LlamaIndex Document."""
    from llama_index.core import Document

    if not path.exists():
        return None
    suffix = path.suffix.lower()
    text = ""
    if suffix in (".txt", ".md", ".csv"):
        text = path.read_text(encoding="utf-8", errors="replace")
    elif suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    else:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None
    if not text.strip():
        return None
    return Document(text=text, metadata={"filename": path.name, "file_path": str(path)})


def index_documents(
    storage_paths: list[Path],
    namespace: str | None = None,
    embed_model_name: str | None = None,
) -> dict[str, Any]:
    """
    Load documents from storage paths, chunk, embed, and upsert into Pinecone.
    Returns dict with chunk_count, doc_count, and any errors.
    """
    from llama_index.core import Settings, StorageContext, VectorStoreIndex

    if not Config.PINECONE_API_KEY or not Config.OPENAI_API_KEY:
        return {"error": "PINECONE_API_KEY and OPENAI_API_KEY must be set"}

    vector_store = _get_vector_store()
    embed_model = _get_embed_model()

    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    Settings.chunk_overlap = 50

    documents = []
    for path in storage_paths:
        if not path.exists():
            logger.warning("Skipping missing path: %s", path)
            continue
        try:
            doc = _load_document(path)
            if doc:
                documents.append(doc)
        except Exception as e:
            logger.exception("Failed to load %s: %s", path, e)
            raise

    if not documents:
        return {"chunk_count": 0, "doc_count": 0, "indexed": False}

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=False,
    )

    return {
        "chunk_count": len(documents),
        "doc_count": len(documents),
        "indexed": True,
    }


def retrieve(query: str, top_k: int | None = None) -> list[dict[str, Any]]:
    """
    Retrieve relevant chunks from Pinecone for a query.
    Returns list of dicts with keys: content, score, metadata.
    """
    from llama_index.core import VectorStoreIndex

    if not Config.PINECONE_API_KEY or not Config.OPENAI_API_KEY:
        return []

    k = top_k or Config.RAG_TOP_K
    vector_store = _get_vector_store()
    embed_model = _get_embed_model()

    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    retriever = index.as_retriever(similarity_top_k=k)
    nodes = retriever.retrieve(query)

    results = []
    for node in nodes:
        results.append(
            {
                "content": node.get_content(),
                "score": getattr(node, "score", None),
                "metadata": node.metadata or {},
            }
        )
    return results
