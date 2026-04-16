import json
import time
from pathlib import Path
from typing import Dict, List

CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)


def _chat_path(chat_id: str) -> Path:
    return CHATS_DIR / f"{chat_id}.json"


def create_chat() -> Dict:
    chat_id = str(int(time.time() * 1000))
    chat = {
        "id": chat_id,
        "title": f"Chat {chat_id[-4:]}",
        "created_at": time.time(),
        "messages": [],
    }
    path = _chat_path(chat_id)
    with path.open("w", encoding="utf-8") as f:
        json.dump(chat, f, ensure_ascii=False, indent=2)
    return chat


def save_chat(chat_id: str, messages: List[Dict[str, str]]) -> None:
    path = _chat_path(chat_id)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            chat = json.load(f)
    else:
        chat = {
            "id": chat_id,
            "title": f"Chat {chat_id[-4:]}",
            "created_at": time.time(),
            "messages": [],
        }
    chat["messages"] = messages
    with path.open("w", encoding="utf-8") as f:
        json.dump(chat, f, ensure_ascii=False, indent=2)


def load_chat(chat_id: str) -> Dict:
    path = _chat_path(chat_id)
    if not path.exists():
        raise FileNotFoundError(f"Chat {chat_id} not found")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_chats() -> List[Dict]:
    chats = []
    for path in sorted(CHATS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        with path.open("r", encoding="utf-8") as f:
            chat = json.load(f)
            chats.append(
                {
                    "id": chat["id"],
                    "title": chat.get("title", chat["id"]),
                    "created_at": chat.get("created_at", 0.0),
                }
            )
    return chats


def delete_chat(chat_id: str) -> None:
    path = _chat_path(chat_id)
    if path.exists():
        path.unlink()
