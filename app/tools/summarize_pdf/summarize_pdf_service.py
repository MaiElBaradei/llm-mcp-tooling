from typing import Iterator, List
from ..extract_pdf_text import ExtractPDFTextTool
from ..summarize_text import SummarizeTextTool
from ..detect_language import DetectLanguageTool
from ...utils import Chunker, decide_chunk_size
import logging

logger = logging.getLogger(__name__)


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
        logger.info("SummarizePDFService initialized")
        

    def summarize(self, pdf_path_or_url: str) -> Iterator[dict]:
        try:
            logger.info(f"Starting PDF summarization process for: {pdf_path_or_url}")
            
            # Extract PDF text
            logger.info("Extracting text from PDF")
            extracted = self.pdf_extractor.run(pdf_path_or_url)
            
            if not extracted.get("success"):
                error_msg = extracted.get("error", "Unknown error")
                logger.error(f"PDF extraction failed: {error_msg}")
                raise ValueError(f"PDF extraction failed: {error_msg}")
            
            if not extracted.get("text"):
                logger.warning("PDF contains no text to summarize")
                yield {
                    "final_summary": "",
                    "metadata": {
                        "pages": extracted.get("pages", 0),
                        "chunks": 0,
                        "language": None,
                        "document_length": 0,
                        "summary_length": 0,
                        "processing_time": 0,
                    },
                }
                return
            
            # Detect language
            logger.info("Detecting document language")
            lang = self.language_detector.run(extracted["text"])["language"]
            chunk_size = decide_chunk_size(lang)
            logger.info(f"Language detected: {lang}, chunk size: {chunk_size}")
            self.chunker = Chunker(chunk_size=chunk_size)

            chunk_summaries: List[str] = []
            self.document_length = 0
            self.summary_length = 0
            self.processing_time = 0

            # Process chunks
            for index, chunk in enumerate(
                self.chunker.chunk_text_with_overlap(text=extracted["text"], overlap=50), start=1
            ):
                try:
                    logger.info(f"Processing chunk {index}")
                    summary_result = self.summarizer.run(chunk)

                    chunk_summary = summary_result["summary"].strip()
                    chunk_summaries.append(chunk_summary)
                    metadata = summary_result.get("metadata", {})
                    self.summary_length += metadata.get("summary_length", 0)
                    self.document_length += metadata.get("document_length", 0)
                    self.processing_time += metadata.get("processing_time", 0)

                    logger.debug(f"Chunk {index} summarized: {len(chunk_summary)} characters")
                    # streaming chunk-level result
                    yield {
                        "chunk": index,
                        "partial_summary": chunk_summary,
                    }
                except Exception as e:
                    logger.error(f"Error processing chunk {index}: {e}", exc_info=True)
                    raise

            final_summary = "\n".join(chunk_summaries)
            logger.info(f"PDF summarization completed: {len(chunk_summaries)} chunks, {len(final_summary)} characters")

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
        except Exception as e:
            logger.error(f"Error in PDF summarization process: {e}", exc_info=True)
            raise
