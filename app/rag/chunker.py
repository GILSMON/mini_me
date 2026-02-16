from app.config import settings


def chunk_markdown(text: str) -> list[dict]:
    """Split markdown into overlapping chunks.

    Returns list of {"text": str, "metadata": {"source": str, "chunk_index": int}}
    """
    size = settings.chunk_size
    overlap = settings.chunk_overlap
    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = start + size
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": {"source": "biography.md", "chunk_index": idx},
                }
            )
            idx += 1
        start += size - overlap

    return chunks
