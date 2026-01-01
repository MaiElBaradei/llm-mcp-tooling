from .metrics import CosineSimilarityMetric
from .metrics import LexicalSimilarityMetric
from .metrics import ConcisenessMetric
import logging

logger = logging.getLogger(__name__)


class EvaluateLLMResponsesService:
    def __init__(self):
        self.cosine = CosineSimilarityMetric()
        self.lexical = LexicalSimilarityMetric()
        self.concise = ConcisenessMetric()
        logger.info("EvaluateLLMResponsesService initialized")

    def evaluate(self, ground_truth: str, response: str) -> dict:
        try:
            logger.info("Computing evaluation metrics for ground truth and response")
            cosine_score = self.cosine.compute(ground_truth, response)
            lexical_score = self.lexical.compute(ground_truth, response)
            conciseness_score = self.concise.compute(ground_truth, response)
            
            result = {
                "cosine_similarity": cosine_score,
                "lexical_similarity": lexical_score,
                "conciseness_score": conciseness_score,
            }
            logger.info(f"Evaluation metrics computed: cosine={cosine_score:.3f}, lexical={lexical_score:.3f}, conciseness={conciseness_score:.3f}")
            return result
        except Exception as e:
            logger.error(f"Error computing evaluation metrics: {e}", exc_info=True)
            raise
