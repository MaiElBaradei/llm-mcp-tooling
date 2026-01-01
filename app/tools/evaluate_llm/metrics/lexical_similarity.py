# similarity/lexical.py
from .interfaces import SimilarityMetric
import logging

logger = logging.getLogger(__name__)


class LexicalSimilarityMetric(SimilarityMetric):
    def compute(self, ground_truth: str, response: str) -> float:
        try:
            logger.debug("Computing lexical similarity")
            gt_tokens = set(ground_truth.lower().split())
            resp_tokens = set(response.lower().split())

            if not gt_tokens or not resp_tokens:
                logger.debug("Empty token sets detected, returning 0.0")
                return 0.0

            intersection = gt_tokens & resp_tokens
            union = gt_tokens | resp_tokens
            score = len(intersection) / len(union)
            logger.debug(f"Lexical similarity computed: {score:.3f}")
            return score
        except Exception as e:
            logger.error(f"Error computing lexical similarity: {e}", exc_info=True)
            raise
