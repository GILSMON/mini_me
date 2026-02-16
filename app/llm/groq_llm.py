from groq import Groq

from app.config import settings
from app.llm.base import LLMClient


class GroqLLM(LLMClient):
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_chat_model

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        context_chunks: list[str],
    ) -> str:
        context = "\n\n---\n\n".join(context_chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Context about me:\n{context}\n\nQuestion: {user_message}",
                },
            ],
        )
        return response.choices[0].message.content
