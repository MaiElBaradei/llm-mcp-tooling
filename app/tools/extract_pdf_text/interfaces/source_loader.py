from abc import ABC, abstractmethod

class SourceLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> str:
        """Returns local PDF path"""
        pass