from flask import Blueprint, jsonify, request

from services.eval_service import EvaluationService

eval_bp = Blueprint('eval_bp', __name__)
eval_service = EvaluationService()

@eval_bp.route('/retrieval', methods=['POST'])
def eval_retrieval():
    data = request.json or {}
    result = eval_service.evaluate_retrieval(data)
    return jsonify(result)

@eval_bp.route('/generation', methods=['POST'])
def eval_generation():
    data = request.json or {}
    result = eval_service.evaluate_generation(data)
    return jsonify(result)

@eval_bp.route('/e2e', methods=['POST'])
def eval_e2e():
    data = request.json or {}
    result = eval_service.evaluate_e2e(data)
    return jsonify(result)

@eval_bp.route('/history/<eval_type>', methods=['GET'])
def get_eval_history(eval_type):
    history = eval_service.get_history(eval_type)
    return jsonify({"eval_type": eval_type, "history": history})
