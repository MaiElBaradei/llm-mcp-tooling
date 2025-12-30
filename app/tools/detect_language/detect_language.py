from .detect_laguage_service import DetectLanguageService
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DetectLanguageTool:
    name = "detect_language"
    description = (
        "Detects the language of a given text string. "
        "Returns the ISO 639-1 language code and confidence score."
    )
    
    def __init__(self):
        self.service = DetectLanguageService()
        logger.info("DetectLanguageTool initialized")

    def run(self, text: str) -> Dict[str, Any]:
        try:
            logger.info(f"Detecting language for text (length: {len(text) if text else 0})")
            result = self.service.detect_language(text)
            logger.info(f"Language detection completed: {result.get('language')} (confidence: {result.get('confidence', 0):.3f})")
            return result
        except Exception as e:
            logger.error(f"Error detecting language: {e}", exc_info=True)
            raise
