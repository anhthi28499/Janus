
from repositories.kb_repository import KnowledgebaseRepository

repo = KnowledgebaseRepository()

class KnowledgebaseService:
    def list_documents(self):
        docs = repo.get_all_documents()
        return [{"id": d.id, "filename": d.filename, "status": d.status, "created_at": d.created_at.isoformat()} for d in docs]

    def upload_document(self, file):
        # In a real app, save 'file' to a bucket or local storage
        # Here we simulate by just recording the filename
        filename = file.filename if hasattr(file, 'filename') else "unknown.txt"
        doc = repo.add_document(filename)
        return {"message": "Document uploaded successfully", "id": doc.id}

    def train_documents(self, config_data):
        # Placeholder for Langchain Pinecone Indexing logic
        # config_data would contain 'embedding_model', 'vector_db' etc.
        docs = repo.get_all_documents()
        for doc in docs:
            if doc.status == 'uploaded':
                repo.update_status(doc.id, 'indexed')

        return {"message": "Knowledgebase training completed successfully", "config_used": config_data}
