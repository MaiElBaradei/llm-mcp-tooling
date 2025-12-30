from abc import ABC, abstractmethod
from typing import Dict


class LLMClient(ABC):
    """
    Abstract LLM client interface.
    """

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> Dict:
        pass
