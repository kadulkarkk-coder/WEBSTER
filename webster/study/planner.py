"""
WEBSTER Study Planner
=====================
Plan study sessions, track progress, and manage schedules.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from webster.core.logger import Logger
from webster.memory.sqlite_store import SQLiteStore


class StudyPlanner:
    """Plan and track study sessions."""

    def __init__(self):
        self.logger = Logger().get_logger("PLANNER")
        self.db = SQLiteStore()

    def create_session(self, subject: str, duration_minutes: int,
                       topic: str = "", date: Optional[str] = None) -> int:
        date = date or datetime.now().isoformat()
        end_time = (datetime.fromisoformat(date) + timedelta(minutes=duration_minutes)).isoformat()
        event_id = self.db.add_event(
            title=f"Study: {subject}",
            start_time=date,
            end_time=end_time,
            description=f"Topic: {topic}\nDuration: {duration_minutes}min",
            color="#7c4dff"
        )
        self.logger.info(f"Study session planned: {subject} ({duration_minutes}min)")
        return event_id

    def get_today_sessions(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_events(
            date_from=f"{today}T00:00:00",
            date_to=f"{today}T23:59:59"
        )

    def get_week_sessions(self) -> List[Dict]:
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return self.db.get_events(
            date_from=start.strftime("%Y-%m-%dT00:00:00"),
            date_to=end.strftime("%Y-%m-%dT23:59:59")
        )

    def suggest_pomodoro(self, subject: str, total_minutes: int) -> List[Dict]:
        pomodoros = []
        sessions = total_minutes // 25
        for i in range(sessions):
            pomodoros.append({
                "session": i + 1,
                "subject": subject,
                "focus_minutes": 25,
                "break_minutes": 5,
                "total": 30,
            })
        return pomodoros

    def get_study_time_today(self) -> int:
        sessions = self.get_today_sessions()
        total = 0
        for session in sessions:
            if session.get("start_time") and session.get("end_time"):
                start = datetime.fromisoformat(session["start_time"])
                end = datetime.fromisoformat(session["end_time"])
                total += (end - start).seconds // 60
        return total

    def get_stats(self) -> dict:
        return {
            "today_minutes": self.get_study_time_today(),
            "today_sessions": len(self.get_today_sessions()),
            "week_sessions": len(self.get_week_sessions()),
        }
