# similarity/cosine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .interfaces import SimilarityMetric
import logging

logger = logging.getLogger(__name__)


class CosineSimilarityMetric(SimilarityMetric):
    def compute(self, ground_truth: str, response: str) -> float:
        try:
            logger.debug("Computing cosine similarity")
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([ground_truth, response])
            score = float(cosine_similarity(vectors[0], vectors[1])[0][0])
            logger.debug(f"Cosine similarity computed: {score:.3f}")
            return score
        except Exception as e:
            logger.error(f"Error computing cosine similarity: {e}", exc_info=True)
            raise
