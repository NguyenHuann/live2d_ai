import requests
from typing import List, Dict
from utils import get_env

SESSIONS: dict[str, list[dict[str, str]]] = {}

SYSTEM_PROMPT = (
    "Bạn là một cô gái tên Hana. Tính cách: thân thiện, vui vẻ, tích cực, năng động, thú vị, "
    "trả lời ngắn gọn, lịch sự, dùng tiếng Việt tự nhiên."
)

OLLAMA_HOST  = get_env("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = get_env("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_K_M")
TEMPERATURE  = float(get_env("LLM_TEMPERATURE", "0.6"))

def get_history(session_id: str) -> List[Dict[str,str]]:
    hist = SESSIONS.setdefault(session_id, [])
    if not hist or hist[0].get("role") != "system":
        hist.insert(0, {"role":"system","content":SYSTEM_PROMPT})
    return hist

def save_turn(session_id: str, role: str, content: str):
    SESSIONS.setdefault(session_id, []).append({"role": role, "content": content})

def chat_with_ollama(session_id: str, user_message: str) -> str:
    hist = get_history(session_id)
    hist.append({"role":"user","content":user_message})

    payload = {
        "model": OLLAMA_MODEL,
        "messages": hist[-20:],
        "options": {"temperature": TEMPERATURE},
        "stream": False
    }
    r = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    ai_text = data.get("message",{}).get("content","").strip() or "Mình đang nghe bạn đây!"
    save_turn(session_id, "assistant", ai_text)
    return ai_text
