from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_message: str,
        context_chunks: list[str],
    ) -> str: ...
