from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    text: str
    metadata: dict
    score: float


class VectorStore(ABC):
    @abstractmethod
    def add_texts(
        self,
        texts: list[str],
        metadatas: list[dict],
        embeddings: list[list[float]],
    ) -> None: ...

    @abstractmethod
    def query(self, embedding: list[float], top_k: int) -> list[SearchResult]: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def clear(self) -> None: ...
