from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .gpt_client import generate_reply
from .signal_engine import get_latest_signals, list_assets
from .tasks import start_scheduler

BASE_DIR = Path(__file__).resolve().parents[1]

app = FastAPI(title="Quantum Trading AI", version="0.1.0")

# Static frontend (served by FastAPI)
frontend_path = BASE_DIR / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

# CORS (allow local dev tools)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

class ChatResponse(BaseModel):
    reply: str

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/assets")
async def assets():
    return {"assets": list_assets()}

@app.get("/api/signals")
async def signals():
    return {"signals": get_latest_signals()}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        answer = await generate_reply(req.message)
        return {"reply": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# kick off background scheduler (hourly self-evaluation, stub)
start_scheduler()
