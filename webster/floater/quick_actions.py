"""
WEBSTER Quick Actions
=====================
Quick action buttons for common tasks from the floating assistant.
"""

from typing import Any, Callable, Dict, List, Optional
from webster.core.logger import Logger


class QuickActions:
    """Quick action commands accessible from the floating assistant."""

    ACTIONS = {
        "search": {"icon": "🔍", "label": "Search Web", "command": "search"},
        "note": {"icon": "📝", "label": "Quick Note", "command": "note"},
        "calc": {"icon": "🔢", "label": "Calculator", "command": "calc"},
        "timer": {"icon": "⏰", "label": "Set Timer", "command": "timer"},
        "remind": {"icon": "🔔", "label": "Reminder", "command": "remind"},
        "open": {"icon": "📂", "label": "Open App", "command": "open"},
        "study": {"icon": "📚", "label": "Study Mode", "command": "study"},
        "mood": {"icon": "🎵", "label": "Focus Music", "command": "mood"},
    }

    def __init__(self):
        self.logger = Logger().get_logger("QUICK_ACT")
        self._handlers: Dict[str, Callable] = {}

    def register(self, action_key: str, handler: Callable):
        self._handlers[action_key] = handler

    def execute(self, action_key: str) -> Any:
        if action_key in self._handlers:
            return self._handlers[action_key]()
        if action_key in self.ACTIONS:
            return {"action": action_key, "command": self.ACTIONS[action_key]["command"]}
        return None

    def get_actions(self) -> List[Dict]:
        return [
            {"key": k, **v} for k, v in self.ACTIONS.items()
        ]
