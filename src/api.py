import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agents.test_crewai_orchestrator import run_orchestrator


load_dotenv()


FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://127.0.0.1:5500",
)


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