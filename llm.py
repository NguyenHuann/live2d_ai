import google.generativeai as genai
from typing import List, Dict
from utils import get_env

SESSIONS: dict[str, list[dict[str, str]]] = {}

SYSTEM_PROMPT = (
    "Bạn là một cô gái tên Hana. Tính cách: thân thiện, vui vẻ, tích cực, năng động, thú vị, "
    "trả lời ngắn gọn, lịch sự, dùng tiếng Việt tự nhiên."
)

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
GEMINI_MODEL = get_env("GEMINI_MODEL", "gemini-pro")
TEMPERATURE = float(get_env("LLM_TEMPERATURE", "0.6"))

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name=GEMINI_MODEL, system_instruction=SYSTEM_PROMPT)

def get_history(session_id: str) -> List[Dict[str, str]]:
    return SESSIONS.setdefault(session_id, [])

def save_turn(session_id: str, role: str, content: str):
    SESSIONS.setdefault(session_id, []).append({"role": role, "content": content})

def chat_with_gemini(session_id: str, user_message: str) -> str:
    hist = get_history(session_id)
    # Exclude current user message from history when sending to Gemini
    conv = [
        {"role": ("model" if m["role"] == "assistant" else m["role"]), "parts": [m["content"]]}
        for m in hist[:-1][-20:]
    ]
    chat = model.start_chat(history=conv)
    response = chat.send_message(user_message, generation_config={"temperature": TEMPERATURE})
    ai_text = (response.text or "Mình đang nghe bạn đây!").strip()
    save_turn(session_id, "assistant", ai_text)
    return ai_text
