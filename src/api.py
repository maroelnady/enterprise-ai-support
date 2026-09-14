import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.agents.test_crewai_orchestrator import run_orchestrator


load_dotenv()

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://127.0.0.1:5500",
)

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"


app = FastAPI(
    title="Enterprise AI Support API",
    description="API for the Enterprise AI Support Assistant",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Enterprise AI Support API",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = run_orchestrator(request.message)

    return ChatResponse(
        response=result
    )


# Serve the Chat UI from FastAPI
# This must come AFTER the API routes above.
app.mount(
    "/",
    StaticFiles(
        directory=str(WEB_DIR),
        html=True,
    ),
    name="web",
)