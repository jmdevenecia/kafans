import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .models import ChatRequest, ChatResponse
from .agent import run_agent
from .ingest import ingest_directory

load_dotenv()

app = FastAPI(title="Research Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "https://your-app.vercel.app")],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

def _require_secret(x_api_secret: str = Header(None)):
    if x_api_secret != os.getenv("API_SECRET"):
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/session")
def new_session():
    return {"session_id": str(uuid.uuid4())}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    result = await run_agent(req.session_id, req.message)
    return ChatResponse(
        session_id=req.session_id,
        reply=result["answer"],
        response_language=result["response_language"],
        sources=result["sources"],
    )

@app.post("/ingest")
async def ingest(path: str, x_api_secret: str = Header(None)):
    """Protected endpoint — run once or when research DB is updated."""
    _require_secret(x_api_secret)
    result = ingest_directory(path)
    return result

# WebSocket for streaming responses
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            result = await run_agent(session_id, message)
            await websocket.send_json({
                "reply": result["answer"],
                "response_language": result["response_language"],
                "sources": result["sources"],
            })
    except WebSocketDisconnect:
        pass