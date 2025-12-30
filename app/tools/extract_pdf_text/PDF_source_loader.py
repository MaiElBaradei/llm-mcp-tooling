import os
import logging
import requests
import tempfile
from .interfaces import SourceLoader

logger = logging.getLogger(__name__)


class PDFSourceLoader(SourceLoader):

    def load(self, source: str) -> str:
        try:
            logger.info(f"Loading PDF from source: {source}")
            if source.startswith(("http://", "https://")):
                result = self._load_from_url(source)
            else:
                result = self._load_from_file(source)
            logger.info(f"PDF source loaded successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Error loading PDF source: {e}", exc_info=True)
            raise

    def _load_from_url(self, url: str) -> str:
        try:
            logger.info(f"Downloading PDF from URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logger.info(f"PDF downloaded successfully, size: {len(response.content)} bytes")

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_file.write(response.content)
            temp_file.close()
            logger.info(f"PDF saved to temporary file: {temp_file.name}")
            return temp_file.name
        except requests.RequestException as e:
            logger.error(f"Error downloading PDF from URL {url}: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error processing downloaded PDF: {e}", exc_info=True)
            raise

    def _load_from_file(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                logger.error("PDF file does not exist: %s", path)
                raise FileNotFoundError(f"File does not exist: {path}")
            
            file_size = os.path.getsize(path)
            logger.info(f"PDF file found: {path}, size: {file_size} bytes")
            return path
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error loading PDF file {path}: {e}", exc_info=True)
            raise
