"""
WEBSTER Memory Summary
======================
Generate summaries of conversations and long-term memory.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from webster.core.logger import Logger


class MemorySummary:
    """Create summaries from memory data."""

    def __init__(self):
        self.logger = Logger().get_logger("MEM_SUMMARY")

    def conversation_summary(self, messages: List[Dict], max_points: int = 5) -> str:
        """Extract key points from a conversation."""
        if not messages:
            return "No conversation history."
        topics = set()
        user_msgs = [m["content"] for m in messages if m.get("role") == "user"]
        for msg in user_msgs:
            words = msg.split()[:10]
            topics.add(" ".join(words[:5]))
        return f"Conversation with {len(messages)} messages across {len(topics)} topics."

    def daily_summary(self, messages: List[Dict], date: str = None) -> str:
        date = date or datetime.now().strftime("%Y-%m-%d")
        day_msgs = [m for m in messages if m.get("timestamp", "").startswith(date)]
        return f"{date}: {len(day_msgs)} messages."

    def memory_stats(self, total_messages: int, total_conversations: int, vector_count: int) -> Dict:
        return {
            "total_messages": total_messages,
            "total_conversations": total_conversations,
            "vector_entries": vector_count,
            "last_updated": datetime.now().isoformat()
        }
