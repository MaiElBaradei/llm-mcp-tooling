from typing import Iterator, Dict
from datetime import datetime, timezone
from .summarize_pdf_schema import SUMMARIZE_PDF_STREAM_OUTPUT_SCHEMA
from .summarize_pdf_service import SummarizePDFService
import logging

logger = logging.getLogger(__name__)


class SummarizePDFTool:
    name = "summarize_pdf"
    description = (
        "Summarizes the content of a PDF file from a local path or HTTP URL. "
        "Returns a streaming summary of the PDF document."
    )

    def __init__(self):
        self.service = SummarizePDFService()
        logger.info("SummarizePDFTool initialized")

    def run(self, pdf_path_or_url: str) -> Iterator[Dict]:
        try:
            logger.info(f"Starting PDF summarization for: {pdf_path_or_url}")
            event_count = 0
            for event in self.service.summarize(pdf_path_or_url):
                event_count += 1
                logger.debug(f"Yielding summarization event {event_count}")
                print(event)
                yield event
            logger.info(f"PDF summarization completed: {event_count} events yielded")
        except Exception as e:
            logger.error(f"Error summarizing PDF: {e}", exc_info=True)
            raise
