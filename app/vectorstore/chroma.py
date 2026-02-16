import chromadb

from app.config import settings
from app.vectorstore.base import SearchResult, VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_texts(
        self,
        texts: list[str],
        metadatas: list[dict],
        embeddings: list[list[float]],
    ) -> None:
        ids = [f"chunk_{i}" for i in range(len(texts))]
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, embedding: list[float], top_k: int) -> list[SearchResult]:
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )
        return [
            SearchResult(text=doc, metadata=meta, score=dist)
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def count(self) -> int:
        return self.collection.count()

    def clear(self) -> None:
        self.client.delete_collection(settings.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
