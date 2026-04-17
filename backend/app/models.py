from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    response_language: str   # "english" | "filipino"
    sources: list[str] = []  # doc titles surfaced from KB