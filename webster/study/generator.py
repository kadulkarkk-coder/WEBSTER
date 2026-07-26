"""
WEBSTER Study Generator
=======================
AI-powered generation of study materials.
"""

from typing import Any, Dict, List, Optional
from webster.core.logger import Logger


class StudyGenerator:
    """Generate study materials using AI."""

    def __init__(self):
        self.logger = Logger().get_logger("STUDY_GEN")

    def generate_notes(self, topic: str, content: str) -> str:
        """Generate summarized notes from content."""
        lines = content.strip().split(".")
        key_points = []
        for i, line in enumerate(lines):
            if line.strip() and len(line) > 20:
                key_points.append(f"• {line.strip()}")
                if len(key_points) >= 10:
                    break
        header = f"# {topic}\n\n"
        return header + "\n".join(key_points) if key_points else header + "No summary available."

    def generate_questions(self, content: str, count: int = 5) -> List[Dict]:
        """Generate practice questions from content."""
        sentences = [s.strip() for s in content.split(".") if len(s.strip()) > 30]
        questions = []
        for i, sentence in enumerate(sentences[:count]):
            words = sentence.split()
            if len(words) > 5:
                key_word = words[len(words) // 2]
                question_text = sentence.replace(key_word, "______", 1)
                questions.append({
                    "id": i + 1,
                    "question": f"What word completes: {question_text}?",
                    "answer": key_word
                })
        return questions

    def generate_flashcards(self, content: str, count: int = 10) -> List[Dict]:
        """Generate flashcards from content."""
        pairs = []
        lines = [l for l in content.split("\n") if ":" in l or "-" in l or "=" in l]
        for line in lines[:count]:
            for sep in [":", "-", "="]:
                if sep in line:
                    parts = line.split(sep, 1)
                    pairs.append({
                        "front": parts[0].strip(),
                        "back": parts[1].strip()
                    })
                    break
        return pairs
