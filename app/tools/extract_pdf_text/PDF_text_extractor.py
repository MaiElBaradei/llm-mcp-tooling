import pdfplumber
from .interfaces import PDFExtractor


class PDFTextExtractor(PDFExtractor):

    def extract(self, pdf_path: str):
        extracted_text = []

        with pdfplumber.open(pdf_path) as pdf:
            pages = len(pdf.pages)

            if pages == 0:
                raise ValueError("PDF has no pages.")

            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)

        full_text = "\n".join(extracted_text).strip()
        return full_text, pages
