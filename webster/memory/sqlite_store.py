"""
WEBSTER SQLite Store (JSON-backed for Python 3.14+)
==================================================
General-purpose key-value and table storage.
Uses JSON files instead of sqlite3 for Python 3.14 compatibility.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class SQLiteStore:
    """
    General-purpose key-value and table storage backed by JSON files.
    API-compatible with the original SQLite-based version.
    """

    def __init__(self, db_path: str = "webster/database/webster.db"):
        self.db_path = db_path
        self._data_dir = Path(db_path).parent if db_path else Path("webster/database")
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._data_file = self._data_dir / "webster_data.json"
        self._data: dict = self._load()

    def _load(self) -> dict:
        if self._data_file.exists():
            try:
                with open(self._data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_data()

    def _save(self):
        with open(self._data_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def _default_data(self) -> dict:
        return {
            "kv_store": {},
            "notes": [],
            "tasks": [],
            "reminders": [],
            "flashcards": [],
            "calendar_events": [],
            "_next_id": {"notes": 1, "tasks": 1, "reminders": 1, "flashcards": 1, "calendar_events": 1},
        }

    def _next_id(self, table: str) -> int:
        nid = self._data["_next_id"].get(table, 1)
        self._data["_next_id"][table] = nid + 1
        return nid

    # ── KV Store ──────────────────────────────────────────

    def kv_get(self, key: str, default: Any = None) -> Any:
        entry = self._data["kv_store"].get(key)
        if entry:
            try:
                return json.loads(entry["value"]) if isinstance(entry["value"], str) else entry["value"]
            except (json.JSONDecodeError, TypeError):
                return entry["value"]
        return default

    def kv_set(self, key: str, value: Any, category: str = "general"):
        val = json.dumps(value) if not isinstance(value, str) else value
        self._data["kv_store"][key] = {
            "key": key, "value": val, "category": category,
            "updated_at": datetime.now().isoformat()
        }
        self._save()

    def kv_delete(self, key: str):
        self._data["kv_store"].pop(key, None)
        self._save()

    # ── Notes ─────────────────────────────────────────────

    def add_note(self, title: str, content: str, category: str = "general", tags: List[str] = None) -> int:
        now = datetime.now().isoformat()
        nid = self._next_id("notes")
        self._data["notes"].append({
            "id": nid, "title": title, "content": content or "",
            "category": category, "tags": json.dumps(tags or []),
            "created_at": now, "updated_at": now, "pinned": 0
        })
        self._save()
        return nid

    def get_notes(self, category: Optional[str] = None) -> List[Dict]:
        notes = self._data["notes"]
        if category:
            notes = [n for n in notes if n["category"] == category]
        return sorted(notes, key=lambda n: (-n["pinned"], n.get("updated_at", "")), reverse=False)

    def delete_note(self, note_id: int):
        self._data["notes"] = [n for n in self._data["notes"] if n["id"] != note_id]
        self._save()

    # ── Tasks ─────────────────────────────────────────────

    def add_task(self, title: str, description: str = "", category: str = "general",
                 priority: int = 0, due_date: Optional[str] = None) -> int:
        now = datetime.now().isoformat()
        tid = self._next_id("tasks")
        self._data["tasks"].append({
            "id": tid, "title": title, "description": description or "",
            "status": "pending", "category": category, "priority": priority,
            "due_date": due_date, "created_at": now, "completed_at": None
        })
        self._save()
        return tid

    def get_tasks(self, status: Optional[str] = None) -> List[Dict]:
        tasks = self._data["tasks"]
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        return sorted(tasks, key=lambda t: (-t["priority"], t.get("created_at", "")), reverse=False)

    def update_task_status(self, task_id: int, status: str):
        for task in self._data["tasks"]:
            if task["id"] == task_id:
                task["status"] = status
                if status == "completed":
                    task["completed_at"] = datetime.now().isoformat()
                break
        self._save()

    # ── Flashcards ─────────────────────────────────────────

    def add_flashcard(self, front: str, back: str, category: str = "general") -> int:
        now = datetime.now().isoformat()
        fid = self._next_id("flashcards")
        self._data["flashcards"].append({
            "id": fid, "front": front, "back": back, "category": category,
            "difficulty": 3, "reviewed_count": 0, "last_reviewed": None, "created_at": now
        })
        self._save()
        return fid

    def get_flashcards(self, category: Optional[str] = None) -> List[Dict]:
        cards = self._data["flashcards"]
        if category:
            cards = [c for c in cards if c["category"] == category]
        return sorted(cards, key=lambda c: c.get("reviewed_count", 0))

    # ── Calendar Events ───────────────────────────────────

    def add_event(self, title: str, start_time: str, end_time: Optional[str] = None,
                  description: str = "", color: str = "#00bcd4") -> int:
        now = datetime.now().isoformat()
        eid = self._next_id("calendar_events")
        self._data["calendar_events"].append({
            "id": eid, "title": title, "description": description or "",
            "start_time": start_time, "end_time": end_time or start_time,
            "all_day": 0, "color": color, "created_at": now
        })
        self._save()
        return eid

    def get_events(self, date_from: Optional[str] = None, date_to: Optional[str] = None) -> List[Dict]:
        events = self._data["calendar_events"]
        if date_from:
            events = [e for e in events if e.get("start_time", "") >= date_from]
        if date_to:
            events = [e for e in events if e.get("start_time", "") <= date_to]
        return sorted(events, key=lambda e: e.get("start_time", ""))

    def delete_event(self, event_id: int):
        self._data["calendar_events"] = [e for e in self._data["calendar_events"] if e["id"] != event_id]
        self._save()

    # ── Utilities ─────────────────────────────────────────

    def get_stats(self) -> dict:
        return {
            "notes": len(self._data["notes"]),
            "tasks": len(self._data["tasks"]),
            "reminders": len(self._data["reminders"]),
            "flashcards": len(self._data["flashcards"]),
            "calendar_events": len(self._data["calendar_events"]),
            "kv_entries": len(self._data["kv_store"]),
        }
