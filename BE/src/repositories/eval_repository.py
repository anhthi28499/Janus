from repositories.models import EvaluationResult
from core.database import db
import json

class EvaluationRepository:
    def get_results_by_type(self, eval_type: str):
        return EvaluationResult.query.filter_by(eval_type=eval_type).order_by(EvaluationResult.created_at.desc()).all()
        
    def save_result(self, eval_type: str, metrics: dict):
        result = EvaluationResult(eval_type=eval_type, metrics=metrics)
        db.session.add(result)
        db.session.commit()
        return result
