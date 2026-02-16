import time

from google import genai
from google.genai.errors import ClientError

from app.config import settings
from app.llm.base import LLMClient


class GeminiLLM(LLMClient):
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_chat_model

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        context_chunks: list[str],
    ) -> str:
        context = "\n\n---\n\n".join(context_chunks)
        prompt = (
            f"{system_prompt}\n\n"
            f"Context about me:\n{context}\n\n"
            f"Question: {user_message}"
        )

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                return response.text
            except ClientError as e:
                if e.status_code == 429 and attempt < 2:
                    time.sleep(10 * (attempt + 1))
                    continue
                raise
