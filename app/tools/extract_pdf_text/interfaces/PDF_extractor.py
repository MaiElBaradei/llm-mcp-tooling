from abc import ABC, abstractmethod
from typing import Tuple

class PDFExtractor(ABC):
    @abstractmethod
    def extract(self, pdf_path: str) -> Tuple[str, int]:
        """Returns (text, number_of_pages)"""
        pass