"""
WEBSTER Conversation Store
============================
Persistent conversation storage using JSON files (SQLite-free for Python 3.14 compatibility).
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

_DATA_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)


class ConversationStore:
    """
    Stores conversation history in JSON files.
    Each conversation is stored as a separate JSON file.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or (_DATA_DIR / "conversations")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # ── CRUD ──────────────────────────────────────────────

    def create_conversation(self, title: str = "New Chat") -> str:
        """Create a new conversation and return its ID."""
        conv_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        conv = {
            "id": conv_id,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": {},
        }
        self._save(conv_id, conv)
        return conv_id

    def get_conversation(self, conv_id: str) -> Optional[Dict[str, Any]]:
        """Get a conversation by ID."""
        path = self.data_dir / f"{conv_id}.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all conversations (summary only)."""
        conversations = []
        for path in sorted(self.data_dir.glob("*.json"), reverse=True):
            conv = self.get_conversation(path.stem)
            if conv:
                conversations.append({
                    "id": conv["id"],
                    "title": conv["title"],
                    "created_at": conv["created_at"],
                    "updated_at": conv["updated_at"],
                    "message_count": len(conv["messages"]),
                })
        return conversations

    def delete_conversation(self, conv_id: str) -> bool:
        """Delete a conversation."""
        path = self.data_dir / f"{conv_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    # ── Messages ──────────────────────────────────────────

    def add_message(self, conv_id: str, role: str, content: str) -> bool:
        """Add a message to a conversation."""
        conv = self.get_conversation(conv_id)
        if not conv:
            return False
        conv["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        conv["updated_at"] = datetime.now().isoformat()
        self._save(conv_id, conv)
        return True

    def get_messages(self, conv_id: str) -> List[Dict[str, str]]:
        """Get all messages for a conversation."""
        conv = self.get_conversation(conv_id)
        if not conv:
            return []
        return conv["messages"]

    def clear_messages(self, conv_id: str) -> bool:
        """Clear all messages in a conversation."""
        conv = self.get_conversation(conv_id)
        if not conv:
            return False
        conv["messages"] = []
        conv["updated_at"] = datetime.now().isoformat()
        self._save(conv_id, conv)
        return True

    # ── Internal ──────────────────────────────────────────

    def _save(self, conv_id: str, data: Dict[str, Any]):
        path = self.data_dir / f"{conv_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all_messages_flat(self) -> List[Dict[str, str]]:
        """Get ALL messages from ALL conversations (for memory search)."""
        all_msgs = []
        for conv in self.list_conversations():
            msgs = self.get_messages(conv["id"])
            all_msgs.extend(msgs)
        return all_msgs

    @property
    def total_messages(self) -> int:
        return sum(c["message_count"] for c in self.list_conversations())

    @property
    def total_conversations(self) -> int:
        return len(self.list_conversations())
