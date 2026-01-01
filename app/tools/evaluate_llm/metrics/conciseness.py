# similarity/conciseness.py
from .interfaces import SimilarityMetric
import logging

logger = logging.getLogger(__name__)


class ConcisenessMetric(SimilarityMetric):
    def compute(self, ground_truth: str, response: str) -> float:
        try:
            logger.debug("Computing conciseness score")
            gt_len = len(ground_truth.split())
            resp_len = len(response.split())

            if resp_len == 0:
                logger.debug("Empty response detected, returning 0.0")
                return 0.0

            ratio = gt_len / resp_len

            # Normalize to [0, 1]
            score = min(1.0, ratio)
            logger.debug(f"Conciseness score computed: {score:.3f}")
            return score
        except Exception as e:
            logger.error(f"Error computing conciseness score: {e}", exc_info=True)
            raise
