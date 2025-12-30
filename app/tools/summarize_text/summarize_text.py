from .summarize_text_service import SummarizationService
from .summarize_text_schema import SummarizeTextOutput
from .interfaces import LLMClient
from .gemini_client import GeminiClient
from .summarize_text_prompt import SYSTEM_SUMMARIZATION_PROMPT
import logging

logger = logging.getLogger(__name__)

class SummarizeTextTool:
    name = "summarize_text"
    description = (
        "Summarizes a given text using an LLM. "
        "Returns a summary along with prompt and metadata information."
    )
    
    def __init__(self, llm_client: LLMClient = GeminiClient(), system_prompt: str = SYSTEM_SUMMARIZATION_PROMPT):
        self.service = SummarizationService(llm_client, system_prompt)
        logger.info("SummarizeTextTool initialized")

    def run(self, text: str) -> SummarizeTextOutput:
        try:
            logger.info(f"Starting text summarization (text length: {len(text) if text else 0})")
            raw = self.service.summarize(text)
            
            if "json" not in raw:
                logger.error("Invalid response from summarization service: missing 'json' key")
                raise ValueError("Invalid response from summarization service: missing 'json' key")
            
            result = SummarizeTextOutput(
                summary=raw["json"]["summary"],
                prompt=raw["json"]["prompt"],
                metadata=raw["json"]["metadata"],
            )
            logger.info(f"Text summarization completed: {len(result.summary)} characters")
            return result
        except Exception as e:
            logger.error(f"Error summarizing text: {e}", exc_info=True)
            raise
