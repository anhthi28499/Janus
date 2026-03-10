from __future__ import annotations

from datetime import datetime

from core.database import db

from repositories.models import DocumentMetadata


class KnowledgebaseRepository:
    def get_all_documents(self):
        return DocumentMetadata.query.order_by(DocumentMetadata.created_at.desc()).all()

    def add_document(
        self,
        filename: str,
        storage_path: str | None = None,
        mime_type: str | None = None,
    ):
        doc = DocumentMetadata(
            filename=filename,
            status="uploaded",
            storage_path=storage_path,
            mime_type=mime_type,
        )
        db.session.add(doc)
        db.session.commit()
        return doc

    def get_document_by_id(self, doc_id: int):
        return DocumentMetadata.query.get(doc_id)

    def get_documents_by_status(self, status: str):
        return DocumentMetadata.query.filter_by(status=status).all()

    def update_status(self, doc_id: int, status: str):
        doc = DocumentMetadata.query.get(doc_id)
        if doc:
            doc.status = status
            db.session.commit()
        return doc

    def mark_processing(self, doc_id: int):
        return self.update_status(doc_id, "processing")

    def mark_indexed(
        self,
        doc_id: int,
        *,
        chunk_count: int | None = None,
        embedding_model: str | None = None,
        namespace: str | None = None,
    ):
        doc = DocumentMetadata.query.get(doc_id)
        if doc:
            doc.status = "indexed"
            doc.indexed_at = datetime.utcnow()
            if chunk_count is not None:
                doc.chunk_count = chunk_count
            if embedding_model is not None:
                doc.embedding_model = embedding_model
            if namespace is not None:
                doc.namespace = namespace
            db.session.commit()
        return doc

    def mark_failed(self, doc_id: int, error: str | None = None):
        doc = DocumentMetadata.query.get(doc_id)
        if doc:
            doc.status = "failed"
            doc.last_error = error
            db.session.commit()
        return doc
