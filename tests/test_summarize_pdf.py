import pytest

from app.tools.summarize_pdf.summarize_pdf_service import SummarizePDFService


class FakeExtracted:
    def __init__(self, text: str, num_pages: int = 1):
        self.text = text
        self.num_pages = num_pages


class FakePDFExtractor:
    def __init__(self, extracted: FakeExtracted):
        self._extracted = extracted

    def extract(self, path_or_url: str) -> FakeExtracted:
        # ignore path_or_url, return prepared object
        return self._extracted


class FakeChunker:
    def __init__(self, chunks):
        # chunks: iterable of chunk strings
        self._chunks = list(chunks)

    def chunk(self, text: str):
        # yield the prepared chunks regardless of the input text
        for c in self._chunks:
            yield c


class FakeSummarizer:
    def summarize(self, text: str) -> dict:
        # return a simple dict containing a text summary derived from the input
        return {"text": f"summary of: {text}"}


def test_summarize_pdf_streaming_and_final():
    extracted = FakeExtracted(text="dummy text", num_pages=3)
    pdf_extractor = FakePDFExtractor(extracted)

    # two chunks emitted by the chunker
    chunker = FakeChunker(["chunk one", "chunk two"])
    summarizer = FakeSummarizer()

    service = SummarizePDFService(pdf_extractor, chunker, summarizer)

    events = list(service.summarize("ignored_path"))

    # Expect two streaming partial summary events + one final summary event
    assert len(events) == 3

    # First event: chunk 1
    assert events[0]["chunk"] == 1
    assert events[0]["partial_summary"] == "summary of: chunk one"

    # Second event: chunk 2
    assert events[1]["chunk"] == 2
    assert events[1]["partial_summary"] == "summary of: chunk two"

    # Final event: contains final_summary and metadata
    final = events[2]
    assert "final_summary" in final
    assert "metadata" in final
    assert final["metadata"]["pages"] == 3
    assert final["metadata"]["chunks"] == 2


def test_summarize_pdf_no_chunks_yields_final_only():
    extracted = FakeExtracted(text="", num_pages=1)
    pdf_extractor = FakePDFExtractor(extracted)

    # chunker yields nothing
    chunker = FakeChunker([])
    summarizer = FakeSummarizer()

    service = SummarizePDFService(pdf_extractor, chunker, summarizer)

    events = list(service.summarize("ignored_path"))

    # Only final summary event should be emitted
    assert len(events) == 1
    final = events[0]
    assert final.get("final_summary", None) == ""
    assert final["metadata"]["pages"] == 1
    assert final["metadata"]["chunks"] == 0
