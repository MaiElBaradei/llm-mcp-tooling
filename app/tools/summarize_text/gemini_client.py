from google.genai import Client, types
from dotenv import load_dotenv
from typing import Dict
from .interfaces import LLMClient
from .summarize_text_schema import SummarizeTextOutput

load_dotenv()

class GeminiClient(LLMClient):
    """
    Gemini LLM client wrapper.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.client = Client()
        self.model = model_name

    def generate(self, system_prompt: str, user_prompt: str) -> Dict:
        prompt = f"""
        SYSTEM:
        {system_prompt}

        USER:
        {user_prompt}
        """

        response = self.client.models.generate_content(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.0,
                response_mime_type= "application/json",
                response_schema= SummarizeTextOutput,
            ),
            contents=user_prompt,
        )

        return {
            "text": response.parsed,
            "model": self.model,
        }
