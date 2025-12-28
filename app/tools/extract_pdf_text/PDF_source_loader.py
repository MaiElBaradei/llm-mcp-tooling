import os
import logging
import requests
import tempfile
from .interfaces import SourceLoader

logger = logging.getLogger(__name__)


class PDFSourceLoader(SourceLoader):

    def load(self, source: str) -> str:
        if source.startswith(("http://", "https://")):
            return self._load_from_url(source)
        return self._load_from_file(source)

    def _load_from_url(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

    def _load_from_file(self, path: str) -> str:
        if not os.path.exists(path):
            logger.error("PDF file does not exist: %s", path)
            raise FileNotFoundError(f"File does not exist: {path}")
        return path
