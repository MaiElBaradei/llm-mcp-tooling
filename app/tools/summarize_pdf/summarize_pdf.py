from typing import Iterator, Dict
from datetime import datetime, timezone
from .summarize_pdf_schema import SummarizePDFStreamOutput
from .summarize_pdf_service import SummarizePDFService


class SummarizePDFTool:
    """
    Tool: summarize_pdf
    -------------------
    LLM-facing wrapper for PDF summarization.
    """

    def __init__(self):
        self.service = SummarizePDFService()

    def run(self, pdf_path_or_url: str) -> Iterator[Dict]:
        for event in self.service.summarize(pdf_path_or_url):
            yield event
