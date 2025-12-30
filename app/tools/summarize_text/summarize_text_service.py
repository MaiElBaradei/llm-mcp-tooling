from .interfaces import LLMClient

class SummarizationService:
    def __init__(self, llm_client: LLMClient, system_prompt: str):
        self.llm_client = llm_client
        self.system_prompt = system_prompt

    def summarize(self, text: str) -> dict:
        if not text.strip():
            raise ValueError("Text is empty.")

        user_prompt = f"Summarize the following text:\n\n{text}"

        return self.llm_client.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )
