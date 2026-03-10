from datetime import datetime

from core.database import db


class ChatSession(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship(
        "ChatMessage", backref="session", lazy=True, cascade="all, delete-orphan"
    )


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(36), db.ForeignKey("chat_sessions.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EvaluationResult(db.Model):
    __tablename__ = "evaluation_results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eval_type = db.Column(db.String(50), nullable=False)  # 'retrieval', 'generation', 'e2e'
    metrics = db.Column(db.JSON, nullable=False)  # Store metrics as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DocumentMetadata(db.Model):
    __tablename__ = "document_metadata"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(
        db.String(50), default="uploaded"
    )  # 'uploaded', 'processing', 'indexed', 'failed'
    storage_path = db.Column(db.String(512), nullable=True)
    mime_type = db.Column(db.String(128), nullable=True)
    chunk_count = db.Column(db.Integer, nullable=True)
    embedding_model = db.Column(db.String(128), nullable=True)
    namespace = db.Column(db.String(128), nullable=True)
    last_error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    indexed_at = db.Column(db.DateTime, nullable=True)
