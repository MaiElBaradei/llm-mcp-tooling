import os
from typing import Dict, Union
from .interfaces import SourceLoader, PDFExtractor


class PDFExtractionService:
    def __init__(
        self,
        loader: SourceLoader,
        extractor: PDFExtractor
    ):
        self.loader = loader
        self.extractor = extractor

    def extract(self, source: str) -> Dict[str, Union[str, int, bool]]:
        pdf_path = None

        try:
            pdf_path = self.loader.load(source)
            text, pages = self.extractor.extract(pdf_path)

            if not text:
                return {
                    "success": True,
                    "text": "",
                    "pages": pages,
                    "error": "PDF contains no extractable text."
                }

            return {
                "success": True,
                "text": text,
                "pages": pages,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "pages": 0,
                "error": str(e)
            }

        finally:
            if source.startswith(("http://", "https://")) and pdf_path:
                try:
                    os.remove(pdf_path)
                except OSError:
                    pass
