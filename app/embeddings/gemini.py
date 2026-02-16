from google import genai

from app.config import settings
from app.embeddings.base import EmbeddingProvider


class GeminiEmbedding(EmbeddingProvider):
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.embedding_model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        result = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config={"task_type": "RETRIEVAL_DOCUMENT"},
        )
        return [e.values for e in result.embeddings]

    def embed_query(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model=self.model,
            contents=[text],
            config={"task_type": "RETRIEVAL_QUERY"},
        )
        return result.embeddings[0].values
