"""
WEBSTER Memory Search
=====================
Search through conversation history and stored memories.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from webster.core.logger import Logger


class MemorySearch:
    """Search across all memory stores."""

    def __init__(self):
        self.logger = Logger().get_logger("MEM_SEARCH")

    def search_conversations(self, query: str, messages: List[Dict], max_results: int = 10) -> List[Dict]:
        """Simple keyword search across conversation messages."""
        results = []
        query_lower = query.lower()
        for msg in messages:
            if query_lower in msg.get("content", "").lower():
                results.append(msg)
                if len(results) >= max_results:
                    break
        return results

    def search_by_date(self, messages: List[Dict], date: str) -> List[Dict]:
        return [m for m in messages if m.get("timestamp", "").startswith(date)]

    def search_by_role(self, messages: List[Dict], role: str) -> List[Dict]:
        return [m for m in messages if m.get("role") == role]

    def recent_messages(self, messages: List[Dict], count: int = 10) -> List[Dict]:
        return messages[-count:]

    def highlight_matches(self, text: str, query: str) -> str:
        """Wrap query matches in highlight markers."""
        return text.replace(query, f"**{query}**")
