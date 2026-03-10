import logging
import secrets
from pathlib import Path

from core.config import Config
from repositories.kb_repository import KnowledgebaseRepository

from services.vector_store_service import index_documents

logger = logging.getLogger(__name__)
repo = KnowledgebaseRepository()


class KnowledgebaseService:
    def _ensure_upload_dir(self) -> Path:
        path = Config.UPLOAD_DIR
        path.mkdir(parents=True, exist_ok=True)
        return path

    def list_documents(self):
        docs = repo.get_all_documents()
        return [
            {
                "id": d.id,
                "filename": d.filename,
                "status": d.status,
                "storage_path": d.storage_path,
                "chunk_count": d.chunk_count,
                "created_at": d.created_at.isoformat(),
                "indexed_at": d.indexed_at.isoformat() if d.indexed_at else None,
                "last_error": d.last_error,
            }
            for d in docs
        ]

    def upload_document(self, file):
        if not hasattr(file, "filename") or not file.filename:
            return {"error": "No file provided"}, 400
        filename = file.filename
        upload_dir = self._ensure_upload_dir()
        safe_name = f"{secrets.token_hex(8)}_{Path(filename).name}"
        storage_path = upload_dir / safe_name
        try:
            file.save(str(storage_path))
        except Exception as e:
            logger.exception("Failed to save upload: %s", e)
            return {"error": f"Failed to save file: {e}"}, 500

        mime_type = getattr(file, "content_type", None) or "application/octet-stream"
        doc = repo.add_document(
            filename=filename,
            storage_path=str(storage_path),
            mime_type=mime_type,
        )
        return {"message": "Document uploaded successfully", "id": doc.id}

    def train_documents(self, config_data):
        embedding_model = (
            config_data.get("embeddingModel", config_data.get("embedding_model"))
            or Config.EMBEDDING_MODEL
        )
        namespace = config_data.get("namespace") or Config.PINECONE_NAMESPACE

        docs = repo.get_documents_by_status("uploaded")
        processed = 0
        failed = 0

        for doc in docs:
            if not doc.storage_path:
                repo.mark_failed(doc.id, "No storage path")
                failed += 1
                continue

            path = Path(doc.storage_path)
            if not path.exists():
                repo.mark_failed(doc.id, f"File not found: {path}")
                failed += 1
                continue

            repo.mark_processing(doc.id)
            try:
                result = index_documents([path], namespace=namespace)
                if result.get("error"):
                    repo.mark_failed(doc.id, result["error"])
                    failed += 1
                else:
                    chunk_count = result.get("chunk_count", 0)
                    repo.mark_indexed(
                        doc.id,
                        chunk_count=chunk_count,
                        embedding_model=embedding_model,
                        namespace=namespace,
                    )
                    processed += 1
            except Exception as e:
                logger.exception("Indexing failed for doc %s: %s", doc.id, e)
                repo.mark_failed(doc.id, str(e))
                failed += 1

        return {
            "message": "Knowledgebase training completed successfully",
            "config_used": config_data,
            "processed": processed,
            "failed": failed,
        }
