from typing import Iterator, List
from ..extract_pdf_text import ExtractPDFTextTool
from ..summarize_text import SummarizeTextTool
from ..detect_language import DetectLanguageTool
from utils import Chunker, decide_chunk_size


class SummarizePDFService:
    """
    Orchestrates PDF extraction, chunking, and summarization.
    Yields streaming summary events for each chunk and a final summary event.
    """

    def __init__(self):
        self.pdf_extractor = ExtractPDFTextTool()
        self.language_detector = DetectLanguageTool()
        self.summarizer = SummarizeTextTool()
        self.chunker = None
        self.document_length = 0
        self.summary_length = 0
        self.processing_time = 0
        

    def summarize(self, pdf_path_or_url: str) -> Iterator[dict]:
        extracted = self.pdf_extractor.run(pdf_path_or_url)
        
        lang = self.language_detector.run(extracted["text"])["language"]
        chunk_size = decide_chunk_size(lang)
        self.chunker = Chunker(chunk_size=chunk_size)

        chunk_summaries: List[str] = []

        for index, chunk in enumerate(
            self.chunker.chunk_text_with_overlap(text=extracted["text"], overlap=50), start=1
        ):
            summary_result = self.summarizer.run(chunk)

            chunk_summary = summary_result.summary.strip()
            chunk_summaries.append(chunk_summary)
            self.summary_length += summary_result.metadata.get("summary_length", 0)
            self.document_length += summary_result.metadata.get("document_length", 0)
            self.processing_time += summary_result.metadata.get("processing_time", 0)

            # streaming chunk-level result
            yield {
                "chunk": index,
                "partial_summary": chunk_summary,
            }

        final_summary = "\n".join(chunk_summaries)

        yield {
            "final_summary": final_summary,
            "metadata": {
                "pages": extracted["pages"],
                "chunks": len(chunk_summaries),
                "language": lang,
                "document_length": self.document_length,
                "summary_length": self.summary_length,
                "processing_time": self.processing_time,
            },
        }
