import logging
from typing import Iterator

logger = logging.getLogger(__name__)


class Chunker:
    def __init__(self, chunk_size: int = 600):
        if chunk_size <= 0:
            logger.error("chunk_size must be > 0 (got %s).", chunk_size)
            raise ValueError("chunk_size must be > 0")
        self.chunk_size = chunk_size

    def chunk_text(self, text: str) -> Iterator[str]:
        """Yield non-overlapping chunks (by words) of at most self.chunk_size words.

        Each yielded chunk is a string of up to `chunk_size` words.
        """
        if not text:
            logger.debug("Empty text provided to chunk_text.")
            return

        words = text.split()
        total = (len(words) + self.chunk_size - 1) // self.chunk_size
        logger.debug("Splitting text into up to %d non-overlapping chunks (chunk_size=%d).", total, self.chunk_size)

        for i in range(0, len(words), self.chunk_size):
            yield " ".join(words[i : i + self.chunk_size])

    def chunk_text_with_overlap(self, text: str, overlap: int) -> Iterator[str]:
        """
        Yield chunks with overlapping words between consecutive chunks.
        `overlap` is number of words shared between consecutive chunks. 0 means no overlap.
        """
        if overlap < 0:
            logger.error("overlap must be >= 0 (got %s).", overlap)
            raise ValueError("overlap must be >= 0")
        if overlap >= self.chunk_size and text:
            logger.error("overlap (%s) must be smaller than chunk_size (%s).", overlap, self.chunk_size)
            raise ValueError("overlap must be smaller than chunk_size")

        if not text:
            logger.debug("Empty text provided to chunk_text_with_overlap.")
            return

        words = text.split()
        if len(words) <= self.chunk_size:
            logger.debug("Text shorter than or equal to chunk_size; yielding single chunk.")
            yield " ".join(words)
            return

        step = self.chunk_size - overlap
        if step <= 0:
            # defensive, though we validated overlap earlier
            logger.error("Computed step must be > 0 (chunk_size=%s, overlap=%s).", self.chunk_size, overlap)
            raise ValueError("Computed step must be > 0")

        # We can't know how many chunks until iteration, but estimate for debug
        logger.debug("Creating overlapping chunks (chunk_size=%d, overlap=%d, step=%d).", self.chunk_size, overlap, step)

        for start in range(0, len(words), step):
            end = start + self.chunk_size
            if end >= len(words):
                yield " ".join(words[start:])
            yield " ".join(words[start:end])
            
