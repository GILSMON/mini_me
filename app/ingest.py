"""Ingest biography data into the vector store.

Usage: python -m app.ingest
"""

from app.config import settings
from app.embeddings.gemini import GeminiEmbedding
from app.rag.chunker import chunk_markdown
from app.vectorstore.chroma import ChromaVectorStore


def ingest():
    with open(settings.data_path) as f:
        raw = f.read()

    chunks = chunk_markdown(raw)
    print(f"Chunked into {len(chunks)} pieces")

    embedder = GeminiEmbedding()
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    print("Generating embeddings via Gemini API...")
    embeddings = embedder.embed_texts(texts)

    store = ChromaVectorStore()
    store.clear()
    store.add_texts(texts, metadatas, embeddings)
    print(f"Stored {store.count()} vectors in ChromaDB")


if __name__ == "__main__":
    ingest()
