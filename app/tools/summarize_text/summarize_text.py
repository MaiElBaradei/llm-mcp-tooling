from .summarize_text_service import SummarizationService
from .summarize_text_schema import SUMMARIZE_TEXT_OUTPUT_SCHEMA
from ...llm.gemini_client import GeminiClient
from .summarize_text_prompt import SYSTEM_SUMMARIZATION_PROMPT
import logging
import jsonschema

logger = logging.getLogger(__name__)

class SummarizeTextTool:
    name = "summarize_text"
    description = (
        "Summarizes a given text using an LLM. "
        "Returns a summary along with prompt and metadata information."
    )
    
    def __init__(self, system_prompt: str = SYSTEM_SUMMARIZATION_PROMPT):
        llm_client = GeminiClient()
        self.service = SummarizationService(llm_client, system_prompt)
        logger.info("SummarizeTextTool initialized")

    def run(self, text: str) -> dict:
        try:
            logger.info(f"Starting text summarization (text length: {len(text) if text else 0})")
            raw = self.service.summarize(text)
            
            if "json" not in raw:
                logger.error("Invalid response from summarization service: missing 'json' key")
                raise ValueError("Invalid response from summarization service: missing 'json' key")
            
            result = raw["json"]
            
            # Validate output against JSON schema
            try:
                jsonschema.validate(instance=result, schema=SUMMARIZE_TEXT_OUTPUT_SCHEMA)
            except jsonschema.ValidationError as e:
                logger.error(f"Output validation failed: {e.message}")
                raise ValueError(f"Invalid output data: {e.message}")
            
            logger.info(f"Text summarization completed: {len(result.get('summary', ''))} characters")
            return result
        except (ValueError, KeyError) as e:
            logger.error(f"Error summarizing text: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error summarizing text: {e}", exc_info=True)
            raise
