from .PDF_extraction_service import PDFExtractionService
from .PDF_source_loader import PDFSourceLoader
from .PDF_text_extractor import PDFTextExtractor
import logging

logger = logging.getLogger(__name__)

class ExtractPDFTextTool:
    name = "extract_pdf_text"
    description = (
        "Extracts text from a PDF file given a local path or HTTP URL. "
        "Returns extracted text and number of pages."
    )

    def __init__(self):
        self.service = PDFExtractionService(
            loader=PDFSourceLoader(),
            extractor=PDFTextExtractor()
        )
        logger.info("ExtractPDFTextTool initialized")

    def run(self, source: str):
        try:
            logger.info(f"Extracting text from PDF source: {source}")
            result = self.service.extract(source)
            if result.get("success"):
                logger.info(f"PDF extraction successful: {result.get('pages', 0)} pages extracted")
            else:
                logger.warning(f"PDF extraction failed: {result.get('error')}")
            return result
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}", exc_info=True)
            raise
