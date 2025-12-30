import pdfplumber
from .interfaces import PDFExtractor
import logging

logger = logging.getLogger(__name__)


class PDFTextExtractor(PDFExtractor):

    def extract(self, pdf_path: str):
        try:
            logger.info(f"Extracting text from PDF: {pdf_path}")
            extracted_text = []

            with pdfplumber.open(pdf_path) as pdf:
                pages = len(pdf.pages)
                logger.info(f"PDF opened successfully, pages: {pages}")

                if pages == 0:
                    logger.error("PDF has no pages")
                    raise ValueError("PDF has no pages.")

                for page_num, page in enumerate(pdf.pages, start=1):
                    try:
                        text = page.extract_text()
                        if text:
                            extracted_text.append(text)
                            logger.debug(f"Extracted text from page {page_num}: {len(text)} characters")
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {e}")

            full_text = "\n".join(extracted_text).strip()
            logger.info(f"Text extraction completed: {len(full_text)} characters from {pages} pages")
            return full_text, pages
        except pdfplumber.exceptions.PDFSyntaxError as e:
            logger.error(f"PDF syntax error while extracting text: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}", exc_info=True)
            raise
