from abc import ABC, abstractmethod


class SimilarityMetric(ABC):
    @abstractmethod
    def compute(self, ground_truth: str, response: str) -> float:
        pass
