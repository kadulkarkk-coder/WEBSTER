"""
WEBSTER Study Progress
======================
Track study progress, streaks, and analytics.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta, date
from webster.core.logger import Logger
from webster.memory.sqlite_store import SQLiteStore


class StudyProgress:
    """Track and analyze study progress over time."""

    def __init__(self):
        self.logger = Logger().get_logger("STUDY_PROG")
        self._store = SQLiteStore()
        self._data: Dict = self._store.get("study_progress", {})

    def log_study(self, subject: str, duration_minutes: int, topic: str = ""):
        today = date.today().isoformat()
        if today not in self._data:
            self._data[today] = {"total_minutes": 0, "subjects": {}}
        self._data[today]["total_minutes"] += duration_minutes
        if subject not in self._data[today]["subjects"]:
            self._data[today]["subjects"][subject] = 0
        self._data[today]["subjects"][subject] += duration_minutes
        self._save()

    def get_today(self) -> Dict:
        today = date.today().isoformat()
        return self._data.get(today, {"total_minutes": 0, "subjects": {}})

    def get_week(self) -> Dict:
        week_data = {}
        for i in range(7):
            d = (date.today() - timedelta(days=i)).isoformat()
            if d in self._data:
                week_data[d] = self._data[d]
        return week_data

    def get_streak(self) -> int:
        streak = 0
        current = date.today()
        while True:
            if current.isoformat() in self._data:
                streak += 1
                current -= timedelta(days=1)
            else:
                break
        return streak

    def total_hours(self) -> float:
        return sum(d["total_minutes"] for d in self._data.values()) / 60

    def _save(self):
        self._store.set("study_progress", self._data)
