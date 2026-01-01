from ...llm.interfaces import LLMClient
from .summarize_text_schema import SUMMARIZE_TEXT_RESPONSE_SCHEMA
import logging
import inspect

logger = logging.getLogger(__name__)

class SummarizationService:
    def __init__(self, llm_client: LLMClient, system_prompt: str):
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        logger.info("SummarizationService initialized")

    def summarize(self, text: str) -> dict:
        try:
            if not text or not text.strip():
                logger.error("Cannot summarize: text is empty")
                raise ValueError("Text is empty.")

            logger.info(f"Generating summary for text (length: {len(text)})")
            user_prompt = f"Summarize the following text:\n\n{text}"

            # Check if the LLM client's generate method accepts response_schema parameter
            # by inspecting its signature
            generate_signature = inspect.signature(self.llm_client.generate)
            params = list(generate_signature.parameters.keys())
            
            if 'response_schema' in params:
                # Client supports schema parameter (e.g., GeminiClient)
                logger.debug("Using LLM client with schema support")
                result = self.llm_client.generate(
                    system_prompt=self.system_prompt,
                    user_prompt=user_prompt,
                    response_schema=SUMMARIZE_TEXT_RESPONSE_SCHEMA,
                    response_type="application/json",
                    temperature=0.0
                )
            else:
                # Base interface - no schema support
                logger.warning("LLM client doesn't support schema parameter, using base interface")
                result = self.llm_client.generate(
                    system_prompt=self.system_prompt,
                    user_prompt=user_prompt,
                )
            
            logger.info("Summary generated successfully")
            return result
        except Exception as e:
            logger.error(f"Error generating summary: {e}", exc_info=True)
            raise
