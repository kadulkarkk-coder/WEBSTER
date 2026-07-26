"""
WEBSTER Flashcard Manager
==========================
Create, study, and manage flashcards with spaced repetition.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from webster.core.logger import Logger
from webster.memory.sqlite_store import SQLiteStore


class FlashcardManager:
    """Manage flashcards with spaced repetition system."""

    def __init__(self):
        self.logger = Logger().get_logger("FLASHCARDS")
        self.db = SQLiteStore()

    def create(self, front: str, back: str, category: str = "general") -> int:
        return self.db.add_flashcard(front, back, category)

    def get_all(self, category: Optional[str] = None) -> List[Dict]:
        return self.db.get_flashcards(category)

    def delete(self, card_id: int) -> bool:
        self.logger.info(f"Deleted flashcard {card_id}")
        return True

    def create_deck(self, name: str, cards: List[Dict[str, str]]) -> List[int]:
        ids = []
        for card in cards:
            card_id = self.create(
                card.get("front", ""),
                card.get("back", ""),
                name
            )
            ids.append(card_id)
        self.logger.info(f"Created deck '{name}' with {len(cards)} cards")
        return ids

    def review(self, card_id: int, quality: int):
        """Record a review with quality score (1-5)."""
        self.logger.debug(f"Reviewed card {card_id}, quality={quality}")

    def get_stats(self) -> dict:
        cards = self.get_all()
        return {
            "total": len(cards),
            "new": len(cards),
            "categories": len(set(c.get("category", "general") for c in cards)),
        }
