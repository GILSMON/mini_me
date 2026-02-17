import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings

CHAT_LOG = Path("./logs/chat_log.jsonl")
CHAT_LOG.parent.mkdir(exist_ok=True)
from app.embeddings.gemini import GeminiEmbedding
from app.llm.gemini import GeminiLLM
from app.llm.groq_llm import GroqLLM
from app.rag.engine import RAGEngine
from app.vectorstore.chroma import ChromaVectorStore

router = APIRouter()


def _get_llm():
    if settings.llm_provider == "groq":
        return GroqLLM()
    return GeminiLLM()


_engine = RAGEngine(
    embedder=GeminiEmbedding(),
    store=ChromaVectorStore(),
    llm=_get_llm(),
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict] = []


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    try:
        result = _engine.ask(req.message)
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            raise HTTPException(status_code=429, detail="Rate limit hit. Please wait a moment and try again.")
        raise HTTPException(status_code=500, detail=str(e))
    with open(CHAT_LOG, "a") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "q": req.message, "a": result["answer"]}) + "\n")

    return ChatResponse(**result)


@router.get("/health")
async def health():
    return {"status": "ok", "vectors": _engine.store.count()}
