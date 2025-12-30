from google.genai import Client, types
from dotenv import load_dotenv
from typing import Dict
from .interfaces import LLMClient
from .summarize_text_schema import SummarizeTextOutput
from .summarize_text_schema import RESPONSE_SCHEMA
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiClient(LLMClient):
    """
    Gemini LLM client wrapper.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        try:
            logger.info(f"Initializing GeminiClient with model: {model_name}")
            self.client = Client()
            self.model = model_name
            logger.info("GeminiClient initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing GeminiClient: {e}", exc_info=True)
            raise

    def generate(self, system_prompt: str, user_prompt: str) -> Dict:
        try:
            logger.info(f"Generating content with Gemini model: {self.model}")
            logger.debug(f"System prompt length: {len(system_prompt)}, User prompt length: {len(user_prompt)}")
            
            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.0,
                    response_mime_type="application/json",
                    response_schema=RESPONSE_SCHEMA,
                ),
                contents=user_prompt,
            )

            if not response or not hasattr(response, 'parsed'):
                logger.error("Invalid response from Gemini API: missing parsed content")
                raise ValueError("Invalid response from Gemini API: missing parsed content")

            result = {
                "json": response.parsed,
                "model": self.model,
            }
            logger.info("Content generated successfully by Gemini")
            return result
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}", exc_info=True)
            raise
