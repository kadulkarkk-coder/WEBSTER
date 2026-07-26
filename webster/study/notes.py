"""
WEBSTER Notes Manager
======================
Manages rich text notes with categories, tags, and AI summaries.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from webster.core.logger import Logger
from webster.memory.sqlite_store import SQLiteStore


class NotesManager:
    """Create, read, update, delete notes with categorization."""

    def __init__(self):
        self.logger = Logger().get_logger("NOTES")
        self.db = SQLiteStore()

    def create(self, title: str, content: str = "", category: str = "general",
               tags: Optional[List[str]] = None) -> int:
        note_id = self.db.add_note(title, content, category, tags)
        self.logger.info(f"Created note: {title} [ID: {note_id}]")
        return note_id

    def get_all(self, category: Optional[str] = None) -> List[Dict]:
        return self.db.get_notes(category)

    def get_by_id(self, note_id: int) -> Optional[Dict]:
        notes = self.db.get_notes()
        for note in notes:
            if note["id"] == note_id:
                note["tags"] = self._parse_tags(note.get("tags", "[]"))
                return note
        return None

    def update(self, note_id: int, title: Optional[str] = None,
               content: Optional[str] = None, category: Optional[str] = None,
               tags: Optional[List[str]] = None) -> bool:
        conn = self.db._conn
        updates = []
        params = []
        if title:
            updates.append("title = ?")
            params.append(title)
        if content:
            updates.append("content = ?")
            params.append(content)
        if category:
            updates.append("category = ?")
            params.append(category)
        if tags:
            updates.append("tags = ?")
            params.append(str(tags))
        if not updates:
            return False
        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(note_id)
        conn.execute(
            f"UPDATE notes SET {', '.join(updates)} WHERE id = ?",
            params
        )
        conn.commit()
        return True

    def delete(self, note_id: int) -> bool:
        self.db.delete_note(note_id)
        return True

    def search(self, query: str) -> List[Dict]:
        conn = self.db._conn
        cursor = conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC",
            (f"%{query}%", f"%{query}%")
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_categories(self) -> List[str]:
        conn = self.db._conn
        cursor = conn.execute("SELECT DISTINCT category FROM notes ORDER BY category")
        return [row["category"] for row in cursor.fetchall()]

    def get_stats(self) -> dict:
        notes = self.get_all()
        return {
            "total": len(notes),
            "categories": len(self.get_categories()),
            "recent": notes[:5] if notes else [],
        }

    def _parse_tags(self, tags_str: str) -> List[str]:
        try:
            import json
            return json.loads(tags_str)
        except:
            return []
