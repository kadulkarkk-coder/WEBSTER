"""
WEBSTER Study Subjects
======================
Manage study subjects and courses.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from webster.core.logger import Logger
from webster.memory.sqlite_store import SQLiteStore


class SubjectManager:
    """Manage study subjects with progress tracking."""

    def __init__(self):
        self.logger = Logger().get_logger("SUBJECTS")
        self._store = SQLiteStore()
        self._subjects: Dict = self._store.get("subjects", {})

    def add(self, name: str, color: str = "#7c4dff", icon: str = "📚") -> Dict:
        if name in self._subjects:
            return self._subjects[name]
        subject = {
            "name": name,
            "color": color,
            "icon": icon,
            "created": datetime.now().isoformat(),
            "sessions": 0,
            "hours": 0.0,
            "topics": []
        }
        self._subjects[name] = subject
        self._save()
        self.logger.info(f"Subject added: {name}")
        return subject

    def remove(self, name: str) -> bool:
        if name in self._subjects:
            del self._subjects[name]
            self._save()
            return True
        return False

    def get(self, name: str) -> Optional[Dict]:
        return self._subjects.get(name)

    def list_all(self) -> List[Dict]:
        return list(self._subjects.values())

    def add_topic(self, subject: str, topic: str):
        if subject in self._subjects:
            if topic not in self._subjects[subject]["topics"]:
                self._subjects[subject]["topics"].append(topic)
                self._save()

    def log_session(self, subject: str, duration_minutes: float):
        if subject in self._subjects:
            self._subjects[subject]["sessions"] += 1
            self._subjects[subject]["hours"] += duration_minutes / 60
            self._save()

    def _save(self):
        self._store.set("subjects", self._subjects)

    def count(self) -> int:
        return len(self._subjects)
