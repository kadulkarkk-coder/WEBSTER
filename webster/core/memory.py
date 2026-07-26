"""
WEBSTER Memory Manager
======================
Central memory system combining conversation memory, user profile,
preferences, and long-term vector storage.
"""

import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from webster.core.logger import Logger
from webster.core.errors import MemoryError
from webster.config.paths import Paths


class MemoryManager:
    """
    Central memory manager for WEBSTER.
    
    Manages:
    - Conversation history
    - User preferences and profile
    - Long-term memory (via vector store)
    - Memory summaries
    """

    def __init__(self):
        self.logger = Logger().get_logger("MEMORY")
        self.paths = Paths()
        self._conversations: Dict[str, List[dict]] = {}
        self._preferences: dict = {}
        self._profile: dict = {}
        self._load_all()
        self.logger.info("Memory manager initialized")

    # ── Loading ────────────────────────────────────────

    def _load_all(self):
        """Load all memory data from disk."""
        self._load_conversations()
        self._load_preferences()
        self._load_profile()

    def _load_conversations(self):
        """Load conversations from disk."""
        conv_file = self.paths.memory / "conversations.json"
        if conv_file.exists():
            try:
                with open(conv_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._conversations = data.get("conversations", {})
                    self.logger.debug(f"Loaded {len(self._conversations)} conversations")
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Failed to load conversations: {e}")
                self._conversations = {}

    def _load_preferences(self):
        """Load user preferences."""
        pref_file = self.paths.memory / "preferences.json"
        if pref_file.exists():
            try:
                with open(pref_file, "r", encoding="utf-8") as f:
                    self._preferences = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._preferences = {}

    def _load_profile(self):
        """Load user profile."""
        profile_file = self.paths.memory / "profile.json"
        if profile_file.exists():
            try:
                with open(profile_file, "r", encoding="utf-8") as f:
                    self._profile = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._profile = self._default_profile()

    def _default_profile(self) -> dict:
        return {
            "name": "User",
            "theme": "dark",
            "language": "en",
            "provider": "gemini",
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
        }

    # ── Saving ────────────────────────────────────────

    def save_all(self):
        """Save all memory data to disk."""
        self._save_conversations()
        self._save_preferences()
        self._save_profile()

    def _save_conversations(self):
        """Save conversations to disk."""
        conv_file = self.paths.memory / "conversations.json"
        try:
            conv_file.parent.mkdir(parents=True, exist_ok=True)
            with open(conv_file, "w", encoding="utf-8") as f:
                json.dump({"conversations": self._conversations}, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"Failed to save conversations: {e}")

    def _save_preferences(self):
        """Save preferences to disk."""
        pref_file = self.paths.memory / "preferences.json"
        try:
            with open(pref_file, "w", encoding="utf-8") as f:
                json.dump(self._preferences, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"Failed to save preferences: {e}")

    def _save_profile(self):
        """Save profile to disk."""
        profile_file = self.paths.memory / "profile.json"
        try:
            with open(profile_file, "w", encoding="utf-8") as f:
                json.dump(self._profile, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"Failed to save profile: {e}")

    # ── Conversation Management ────────────────────────

    def start_conversation(self) -> str:
        """Start a new conversation session."""
        conv_id = str(uuid.uuid4())
        self._conversations[conv_id] = []
        return conv_id

    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to a conversation."""
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []
        
        self._conversations[conversation_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._save_conversations()

    def add_user_message(self, message: str, conversation_id: str = None):
        """Add a user message to current or new conversation."""
        if not conversation_id:
            if not self._conversations:
                conversation_id = self.start_conversation()
            else:
                conversation_id = list(self._conversations.keys())[-1]
        self.add_message(conversation_id, "user", message)

    def add_assistant_message(self, message: str, conversation_id: str = None):
        """Add an assistant message to current or new conversation."""
        if not conversation_id:
            if not self._conversations:
                conversation_id = self.start_conversation()
            else:
                conversation_id = list(self._conversations.keys())[-1]
        self.add_message(conversation_id, "assistant", message)

    def get_conversation(self, conversation_id: str) -> List[dict]:
        """Get messages from a conversation."""
        return self._conversations.get(conversation_id, [])

    def get_recent_conversations(self, limit: int = 5) -> List[dict]:
        """Get most recent conversations."""
        sorted_ids = sorted(
            self._conversations.keys(),
            key=lambda cid: self._conversations[cid][-1]["timestamp"] if self._conversations[cid] else "",
            reverse=True
        )
        result = []
        for cid in sorted_ids[:limit]:
            messages = self._conversations[cid]
            if messages:
                result.append({
                    "id": cid,
                    "preview": messages[-1]["content"][:100] if messages else "",
                    "count": len(messages),
                    "last_updated": messages[-1]["timestamp"] if messages else "",
                })
        return result

    def get_all_messages(self, limit: int = 50) -> List[dict]:
        """Get all messages from all conversations, flattened."""
        all_msgs = []
        for conv_id, messages in self._conversations.items():
            for msg in messages:
                all_msgs.append({**msg, "conversation_id": conv_id})
        
        all_msgs.sort(key=lambda m: m.get("timestamp", ""), reverse=True)
        return all_msgs[:limit]

    def delete_conversation(self, conversation_id: str):
        """Delete a conversation."""
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            self._save_conversations()

    def clear_all_conversations(self):
        """Clear all conversations."""
        self._conversations = {}
        self._save_conversations()

    # ── Preferences ────────────────────────────────────

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        return self._preferences.get(key, default)

    def set_preference(self, key: str, value: Any):
        """Set a user preference."""
        self._preferences[key] = value
        self._save_preferences()

    def get_all_preferences(self) -> dict:
        return self._preferences.copy()

    # ── Profile ────────────────────────────────────────

    def get_profile(self) -> dict:
        return self._profile.copy()

    def get_profile_field(self, key: str, default: Any = None) -> Any:
        return self._profile.get(key, default)

    def set_profile_field(self, key: str, value: Any):
        self._profile[key] = value
        self._profile["last_active"] = datetime.now().isoformat()
        self._save_profile()

    def get_user_name(self) -> str:
        return self._profile.get("name", "User")

    def set_user_name(self, name: str):
        self.set_profile_field("name", name)

    # ── Memory Search ──────────────────────────────────

    def search_memory(self, query: str, limit: int = 10) -> List[dict]:
        """Search through all memories for relevant content."""
        results = []
        query_lower = query.lower()
        
        # Search conversations
        for conv_id, messages in self._conversations.items():
            for msg in messages:
                if query_lower in msg["content"].lower():
                    results.append({
                        "type": "conversation",
                        "conversation_id": conv_id,
                        "role": msg["role"],
                        "content": msg["content"][:200],
                        "timestamp": msg["timestamp"],
                        "score": 1.0
                    })
        
        results.sort(key=lambda r: r.get("score", 0), reverse=True)
        return results[:limit]

    # ── Summary ────────────────────────────────────────

    def get_conversation_summary(self, conversation_id: str) -> str:
        """Get a summary of a conversation."""
        messages = self._conversations.get(conversation_id, [])
        if not messages:
            return "No messages in this conversation."
        
        user_msgs = [m for m in messages if m["role"] == "user"]
        assistant_msgs = [m for m in messages if m["role"] == "assistant"]
        
        return (
            f"Conversation: {len(messages)} messages\n"
            f"User: {len(user_msgs)} messages\n"
            f"Spidey: {len(assistant_msgs)} messages\n"
            f"Started: {messages[0]['timestamp'] if messages else 'N/A'}\n"
            f"Last: {messages[-1]['timestamp'] if messages else 'N/A'}"
        )

    def memory_stats(self) -> dict:
        """Get memory statistics."""
        total_messages = sum(len(msgs) for msgs in self._conversations.values())
        return {
            "conversations": len(self._conversations),
            "total_messages": total_messages,
            "preferences_count": len(self._preferences),
            "profile_fields": len(self._profile),
        }

    # ── Lifecycle ──────────────────────────────────────

    def initialize(self):
        """Initialize memory system."""
        self._load_all()
        self.logger.info("Memory system initialized")

    def shutdown(self):
        """Shutdown memory system."""
        self.save_all()
        self.logger.info("Memory system shut down")
