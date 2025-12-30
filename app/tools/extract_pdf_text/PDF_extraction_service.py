import os
from typing import Dict, Union
from .interfaces import SourceLoader, PDFExtractor
import logging

logger = logging.getLogger(__name__)


class PDFExtractionService:
    def __init__(
        self,
        loader: SourceLoader,
        extractor: PDFExtractor
    ):
        self.loader = loader
        self.extractor = extractor
        logger.info("PDFExtractionService initialized")

    def extract(self, source: str) -> Dict[str, Union[str, int, bool]]:
        pdf_path = None

        try:
            logger.info(f"Loading PDF from source: {source}")
            pdf_path = self.loader.load(source)
            logger.info(f"PDF loaded successfully, extracting text")
            text, pages = self.extractor.extract(pdf_path)

            if not text:
                logger.warning("PDF contains no extractable text")
                return {
                    "success": True,
                    "text": "",
                    "pages": pages,
                    "error": "PDF contains no extractable text."
                }

            logger.info(f"Text extraction successful: {pages} pages, {len(text)} characters")
            return {
                "success": True,
                "text": text,
                "pages": pages,
                "error": None
            }

        except Exception as e:
            logger.error(f"Error extracting PDF: {e}", exc_info=True)
            return {
                "success": False,
                "text": "",
                "pages": 0,
                "error": str(e)
            }

        finally:
            if source.startswith(("http://", "https://")) and pdf_path:
                try:
                    logger.debug(f"Cleaning up temporary file: {pdf_path}")
                    os.remove(pdf_path)
                except OSError as e:
                    logger.warning(f"Failed to remove temporary file {pdf_path}: {e}")
