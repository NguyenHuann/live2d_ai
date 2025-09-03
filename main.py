from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

from utils import init_env_and_dirs
from models import ChatRequest, ChatResponse
from llm import chat_with_ollama, save_turn
from tts import synthesize_mp3

init_env_and_dirs()
app = FastAPI(title="AI Live2D Backend (Ollama + gTTS)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def index():
    idx = STATIC_DIR / "index.html"
    return FileResponse(idx) if idx.exists() else {"msg": "Put index.html in /static"}

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/api/chat", response_model=ChatResponse)
async def api_chat(req: ChatRequest, request: Request):
    sid = req.session_id or request.client.host
    try:
        save_turn(sid, "user", req.message)
        ai_text = chat_with_ollama(sid, req.message)
        mp3_path = synthesize_mp3(ai_text)
        if not mp3_path.exists() or mp3_path.stat().st_size < 128:
            raise RuntimeError("Audio file empty.")
        return ChatResponse(text=ai_text, audio_url=f"/static/audio/{mp3_path.name}")
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"{type(e).__name__}: {e}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
