from typing import Optional, Dict, Any
from langdetect import detect_langs, DetectorFactory
import logging

logger = logging.getLogger(__name__)

class DetectLanguageService:
    
    def __init__(self) -> None:
        pass

    def detect_language(self, text: str) -> Dict[str, Optional[Any]]:
        """
        Detect the language of the given text.

        Returns a dict with keys:
        - language: ISO 639-1 code (e.g. 'en', 'fr', 'zh') or None/'und' if unknown
        - confidence: float in [0.0, 1.0] estimating confidence of the detection
        """
        if not text or not text.strip():
            return {"language": None, "confidence": 0.0}

        try:
            DetectorFactory.seed = 0
            probs = detect_langs(text)
            if probs:
                top = probs[0]
                return {"language": top.lang, "confidence": float(top.prob)}
        except Exception as e:
            logger.exception("Language detection failed for input text: %r", text)
            return {"language": None, "confidence": 0.0}

        