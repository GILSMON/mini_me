from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    chroma_persist_dir: str = "./chroma_data"
    collection_name: str = "biography"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3
    embedding_model: str = "gemini-embedding-001"
    data_path: str = "./data/biography.md"

    # LLM provider: "groq" or "gemini"
    llm_provider: str = "groq"

    # Gemini (kept for easy toggle)
    gemini_chat_model: str = "gemini-2.0-flash"

    # Groq
    groq_api_key: str = ""
    groq_chat_model: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = ".env"


settings = Settings()
