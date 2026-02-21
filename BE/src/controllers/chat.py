from flask import Blueprint, request, jsonify
from services.chat_service import ChatService

chat_bp = Blueprint('chat_bp', __name__)
chat_service = ChatService()

@chat_bp.route('/', methods=['POST'])
def send_message():
    data = request.json or {}
    message = data.get('message')
    session_id = data.get('session_id')
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
        
    result = chat_service.chat(session_id, message)
    return jsonify(result)

@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    history = chat_service.get_history(session_id)
    return jsonify({"session_id": session_id, "messages": history})
