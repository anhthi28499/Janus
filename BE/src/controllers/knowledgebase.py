from flask import Blueprint, request, jsonify
from services.kb_service import KnowledgebaseService

kb_bp = Blueprint('kb_bp', __name__)
kb_service = KnowledgebaseService()

@kb_bp.route('/documents', methods=['GET'])
def list_documents():
    docs = kb_service.list_documents()
    return jsonify({"documents": docs})

@kb_bp.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    result = kb_service.upload_document(file)
    return jsonify(result)

@kb_bp.route('/train', methods=['POST'])
def train():
    data = request.json or {}
    result = kb_service.train_documents(data)
    return jsonify(result)
