from .detect_laguage_service import DetectLanguageService
from typing import Dict, Any

class DetectLanguageTool:
    
    def __init__(self):
        self.service = DetectLanguageService()

    def run(self, text: str) -> Dict[str, Any]:
        return self.service.detect_language(text)
