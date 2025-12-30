from .summarize_text_service import SummarizationService
from .summarize_text_schema import SummarizeTextOutput
from .interfaces import LLMClient
from .gemini_client import GeminiClient
from .summarize_text_prompt import SYSTEM_SUMMARIZATION_PROMPT

class SummarizeTextTool:
    def __init__(self, llm_client: LLMClient = GeminiClient(), system_prompt: str = SYSTEM_SUMMARIZATION_PROMPT):
        self.service = SummarizationService(llm_client, system_prompt)

    def run(self, text: str) -> SummarizeTextOutput:
        raw = self.service.summarize(text)
        print(raw)

        return SummarizeTextOutput(
            summary=raw["text"].summary,
            prompt=raw["text"].prompt,
            metadata=raw["text"].metadata,
        )
