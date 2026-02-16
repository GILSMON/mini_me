from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(title="Mini Me")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.streamlit.app",
        "http://localhost:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Mini Me API is running. Use /api/chat to interact."}
