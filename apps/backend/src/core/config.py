import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://janus:janus_pass@localhost:5432/janus_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "janus-kb")
    PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "default")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))

    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "data/uploads")).resolve()

    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
