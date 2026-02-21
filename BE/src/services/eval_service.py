from repositories.eval_repository import EvaluationRepository

repo = EvaluationRepository()

class EvaluationService:
    def evaluate_retrieval(self, data: dict):
        # Placeholder for RAGAS or similar evaluation framework
        # Takes in queries and contexts, outputs metrics like precision, recall
        score = {"precision": 0.85, "recall": 0.90, "f1": 0.87}
        result = repo.save_result("retrieval", score)
        return {"message": "Retrieval evaluation completed", "metrics": score, "id": result.id}
        
    def evaluate_generation(self, data: dict):
        # Placeholder for generation evaluation logic
        score = {"bleu": 0.45, "rougeL": 0.60, "faithfulness": 0.92}
        result = repo.save_result("generation", score)
        return {"message": "Generation evaluation completed", "metrics": score, "id": result.id}
        
    def evaluate_e2e(self, data: dict):
        # Placeholder for End-to-End evaluation logic
        score = {"answer_relevancy": 0.88, "context_precision": 0.82}
        result = repo.save_result("e2e", score)
        return {"message": "End-to-End evaluation completed", "metrics": score, "id": result.id}

    def get_history(self, eval_type: str):
        results = repo.get_results_by_type(eval_type)
        return [{"id": r.id, "metrics": r.metrics, "created_at": r.created_at.isoformat()} for r in results]
