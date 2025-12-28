from .PDF_extraction_service import PDFExtractionService
from .PDF_source_loader import PDFSourceLoader
from .PDF_text_extractor import PDFTextExtractor

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

    def run(self, source: str):
        return self.service.extract(source)
