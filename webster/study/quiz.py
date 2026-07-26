"""
WEBSTER Quiz Generator
======================
Generates quizzes from notes, PDFs, or custom input.
"""

import random
from typing import Any, Dict, List, Optional
from webster.core.logger import Logger


class QuizGenerator:
    """Generate and manage quizzes."""

    def __init__(self):
        self.logger = Logger().get_logger("QUIZ")

    def generate(self, questions: List[Dict[str, Any]], title: str = "Quiz", num_questions: int = None) -> Dict:
        """Generate a quiz from a list of question data."""
        if num_questions and num_questions < len(questions):
            questions = random.sample(questions, num_questions)
        quiz = {
            "title": title,
            "questions": questions,
            "total": len(questions),
            "time_limit_minutes": len(questions) * 1,
            "shuffled": True,
        }
        return quiz

    def multiple_choice(self, question: str, options: List[str], correct: int) -> Dict:
        """Create a multiple-choice question."""
        return {
            "type": "multiple_choice",
            "question": question,
            "options": options,
            "correct": correct,
            "points": 1,
        }

    def true_false(self, question: str, answer: bool) -> Dict:
        """Create a true/false question."""
        return {
            "type": "true_false",
            "question": question,
            "correct": answer,
            "options": ["True", "False"],
            "points": 1,
        }

    def short_answer(self, question: str, answer: str) -> Dict:
        """Create a short answer question."""
        return {
            "type": "short_answer",
            "question": question,
            "correct": answer,
            "points": 2,
        }

    def grade(self, answers: List[Dict]) -> Dict:
        """Grade a completed quiz."""
        correct = 0
        total = len(answers)
        results = []
        for answer in answers:
            is_correct = answer.get("selected") == answer.get("correct")
            if is_correct:
                correct += 1
            results.append({
                "question": answer.get("question", ""),
                "selected": answer.get("selected"),
                "correct": answer.get("correct"),
                "is_correct": is_correct,
            })
        score = (correct / total * 100) if total > 0 else 0
        return {
            "score": round(score, 1),
            "correct": correct,
            "total": total,
            "results": results,
            "passed": score >= 60,
            "grade": self._letter_grade(score),
        }

    def _letter_grade(self, score: float) -> str:
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        if score >= 60: return "D"
        return "F"
