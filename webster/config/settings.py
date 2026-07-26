"""
WEBSTER Settings Manager
========================
Loads and manages application settings with validation.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


class Settings:
    """Global settings manager for WEBSTER."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._base_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self._config_path = self._base_path / "config" / "settings.json"
        self._data: dict = {}
        self._load()

    def _load(self):
        """Load settings from config file."""
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = self._defaults()
        else:
            self._data = self._defaults()
            self._save()

    def _defaults(self) -> dict:
        return {
            "app_name": "WEBSTER",
            "version": "0.1.0",
            "theme": "dark",
            "debug": True,
            "language": "en",
            "window": {
                "width": 1600,
                "height": 900,
                "maximized": False
            },
            "ai": {
                "provider": "gemini",
                "model": "gemini-2.0-flash",
                "temperature": 0.7,
                "max_tokens": 4096,
                "streaming": True
            },
            "voice": {
                "enabled": True,
                "wake_word": True,
                "stt_engine": "whisper",
                "tts_engine": "edge",
                "language": "en-US"
            },
            "study": {
                "pomodoro_duration": 25,
                "short_break": 5,
                "long_break": 15,
                "daily_goal_hours": 4
            },
            "memory": {
                "max_conversations": 100,
                "vector_search": True,
                "auto_summarize": True
            },
            "automation": {
                "browser": True,
                "files": True,
                "system": True
            },
            "plugins": {
                "enabled": True,
                "auto_load": True
            },
            "dashboard": {
                "port": 8501,
                "enabled": True
            },
            "sync": {
                "enabled": False,
                "cloud": False,
                "auto_sync": False
            }
        }

    def _save(self):
        """Save settings to config file."""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
        except IOError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting by dot-notation key."""
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any):
        """Set a setting by dot-notation key."""
        keys = key.split(".")
        target = self._data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self._save()

    def get_all(self) -> dict:
        """Get all settings as dict."""
        return self._data.copy()

    def reset(self):
        """Reset to defaults."""
        self._data = self._defaults()
        self._save()

    @property
    def theme(self) -> str:
        return self._data.get("theme", "dark")

    @theme.setter
    def theme(self, value: str):
        self._data["theme"] = value
        self._save()

    @property
    def ai_provider(self) -> str:
        return self._data.get("ai", {}).get("provider", "gemini")

    @ai_provider.setter
    def ai_provider(self, value: str):
        self._data.setdefault("ai", {})["provider"] = value
        self._save()

    @property
    def debug(self) -> bool:
        return self._data.get("debug", True)

    @property
    def window_width(self) -> int:
        return self._data.get("window", {}).get("width", 1600)

    @property
    def window_height(self) -> int:
        return self._data.get("window", {}).get("height", 900)
