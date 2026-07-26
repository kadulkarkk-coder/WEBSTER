"""
WEBSTER User Preferences
========================
Store and retrieve user preferences and settings.
"""

from typing import Any, Dict, Optional
from webster.core.logger import Logger
from webster.memory.sqlite_store import SQLiteStore


class UserPreferences:
    """Per-user preference storage."""

    DEFAULTS = {
        "theme": "dark",
        "language": "en",
        "voice_enabled": True,
        "wake_word_enabled": True,
        "auto_save": True,
        "streaming": True,
        "provider": "gemini",
        "temperature": 0.7,
        "max_tokens": 4096,
    }

    def __init__(self):
        self.logger = Logger().get_logger("PREFS")
        self._store = SQLiteStore()
        self._prefs: Dict[str, Any] = {}
        self._load()

    def _load(self):
        saved = self._store.get("preferences", {})
        self._prefs = {**self.DEFAULTS, **saved}

    def get(self, key: str, default: Any = None) -> Any:
        return self._prefs.get(key, default)

    def set(self, key: str, value: Any):
        self._prefs[key] = value
        self._save()

    def set_many(self, items: Dict):
        self._prefs.update(items)
        self._save()

    def _save(self):
        self._store.set("preferences", self._prefs)

    def reset(self):
        self._prefs = dict(self.DEFAULTS)
        self._save()

    def export(self) -> Dict:
        return dict(self._prefs)

    def import_prefs(self, data: Dict):
        self._prefs.update(data)
        self._save()
