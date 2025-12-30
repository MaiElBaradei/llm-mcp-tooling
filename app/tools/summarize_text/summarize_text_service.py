from .interfaces import LLMClient
import logging

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

            result = self.llm_client.generate(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
            )
            logger.info("Summary generated successfully")
            return result
        except Exception as e:
            logger.error(f"Error generating summary: {e}", exc_info=True)
            raise
