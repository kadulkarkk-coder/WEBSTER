"""
WEBSTER Context Manager
=======================
Manages contextual information across conversations and sessions.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from webster.core.logger import Logger


@dataclass
class ContextEntry:
    """A single context entry."""
    key: str
    value: Any
    source: str = "system"
    timestamp: float = field(default_factory=time.time)
    ttl: Optional[float] = None  # Time to live in seconds


class ContextManager:
    """
    Manages contextual information across the application.
    
    Tracks:
    - Current conversation context
    - User preferences
    - Session state
    - Cross-module shared context
    """

    def __init__(self):
        self.logger = Logger().get_logger("CONTEXT")
        self._entries: Dict[str, ContextEntry] = {}
        self._session_id = str(uuid.uuid4())[:8]
        self._history: List[dict] = []
        self._max_history = 100
        self.logger.info(f"Context manager initialized (session: {self._session_id})")

    def set(self, key: str, value: Any, source: str = "system", ttl: Optional[float] = None):
        """Set a context value."""
        self._entries[key] = ContextEntry(key=key, value=value, source=source, ttl=ttl)
        self._history.append({"action": "set", "key": key, "source": source, "timestamp": time.time()})
        self._trim_history()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a context value."""
        entry = self._entries.get(key)
        if entry is None:
            return default
        if entry.ttl and (time.time() - entry.timestamp) > entry.ttl:
            del self._entries[key]
            return default
        return entry.value

    def get_all(self) -> Dict[str, Any]:
        """Get all non-expired context entries."""
        now = time.time()
        result = {}
        for key, entry in list(self._entries.items()):
            if entry.ttl and (now - entry.timestamp) > entry.ttl:
                del self._entries[key]
            else:
                result[key] = entry.value
        return result

    def delete(self, key: str):
        """Delete a context entry."""
        if key in self._entries:
            del self._entries[key]
            self._history.append({"action": "delete", "key": key, "timestamp": time.time()})

    def clear(self):
        """Clear all context."""
        self._entries.clear()
        self._history.append({"action": "clear", "timestamp": time.time()})

    def has(self, key: str) -> bool:
        """Check if a context key exists and is valid."""
        return self.get(key) is not None

    def update(self, data: Dict[str, Any], source: str = "system"):
        """Update multiple context values at once."""
        for key, value in data.items():
            self.set(key, value, source)

    def get_session_id(self) -> str:
        return self._session_id

    def get_conversation_context(self) -> Dict[str, Any]:
        """Get context relevant to conversation."""
        keys = ["user_name", "topic", "mood", "last_intent", "current_page", "referrer"]
        return {k: self.get(k) for k in keys if self.has(k)}

    def set_conversation_context(self, user_message: str, ai_response: str):
        """Update context based on conversation."""
        self.set("last_user_message", user_message, source="chat")
        self.set("last_ai_response", ai_response, source="chat")
        self.set("last_interaction", time.time(), source="chat")

    def get_history(self, limit: int = 10) -> List[dict]:
        """Get recent context changes."""
        return self._history[-limit:]

    def _trim_history(self):
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

    def status(self) -> dict:
        return {
            "session_id": self._session_id,
            "active_entries": len(self._entries),
            "history_size": len(self._history),
        }
