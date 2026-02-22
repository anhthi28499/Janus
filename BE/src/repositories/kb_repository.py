from core.database import db
from repositories.models import DocumentMetadata


class KnowledgebaseRepository:
    def get_all_documents(self):
        return DocumentMetadata.query.order_by(DocumentMetadata.created_at.desc()).all()

    def add_document(self, filename: str):
        doc = DocumentMetadata(filename=filename, status='uploaded')
        db.session.add(doc)
        db.session.commit()
        return doc

    def update_status(self, doc_id: int, status: str):
        doc = DocumentMetadata.query.get(doc_id)
        if doc:
            doc.status = status
            db.session.commit()
        return doc
