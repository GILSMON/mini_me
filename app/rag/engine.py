from app.embeddings.base import EmbeddingProvider
from app.llm.base import LLMClient
from app.rag.prompt import SYSTEM_PROMPT
from app.vectorstore.base import VectorStore


class RAGEngine:
    def __init__(
        self,
        embedder: EmbeddingProvider,
        store: VectorStore,
        llm: LLMClient,
    ):
        self.embedder = embedder
        self.store = store
        self.llm = llm

    def ask(self, question: str, top_k: int = 3) -> dict:
        query_vec = self.embedder.embed_query(question)
        results = self.store.query(query_vec, top_k)
        context_chunks = [r.text for r in results]
        answer = self.llm.generate(SYSTEM_PROMPT, question, context_chunks)

        return {
            "answer": answer,
            "sources": [
                {"text": r.text[:100] + "...", "score": r.score}
                for r in results
            ],
        }
