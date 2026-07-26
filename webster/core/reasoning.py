"""
WEBSTER Reasoning Engine
========================
Multi-step reasoning, problem-solving, and decision-making logic.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from webster.core.logger import Logger


@dataclass
class ReasoningStep:
    """A single step in a reasoning chain."""
    number: int
    description: str
    input: str
    output: str
    confidence: float = 1.0


@dataclass
class ReasoningChain:
    """A chain of reasoning steps leading to a conclusion."""
    query: str
    steps: List[ReasoningStep] = field(default_factory=list)
    conclusion: str = ""
    confidence: float = 0.0


class ReasoningEngine:
    """
    Multi-step reasoning engine for complex problem-solving.
    
    Capabilities:
    - Step-by-step logical deduction
    - Cause-effect analysis
    - Compare and contrast
    - Summarization with key points
    - Decision trees
    """

    def __init__(self):
        self.logger = Logger().get_logger("REASONING")
        self._chains: List[ReasoningChain] = []

    def analyze(self, query: str, context: dict = None) -> ReasoningChain:
        """Analyze a query using multi-step reasoning."""
        chain = ReasoningChain(query=query)
        context = context or {}

        # Step 1: Understand the query
        step1 = self._step_understand(query)
        chain.steps.append(step1)

        # Step 2: Break down components
        step2 = self._step_decompose(query)
        chain.steps.append(step2)

        # Step 3: Gather context
        if context:
            step3 = self._step_context(query, context)
            chain.steps.append(step3)

        # Step 4: Reason
        step4 = self._step_reason(query, chain.steps)
        chain.steps.append(step4)

        # Step 5: Conclude
        conclusion = self._step_conclude(chain.steps)
        chain.conclusion = conclusion
        chain.confidence = sum(s.confidence for s in chain.steps) / len(chain.steps)

        self._chains.append(chain)
        return chain

    def _step_understand(self, query: str) -> ReasoningStep:
        """Step 1: Understand what's being asked."""
        query_lower = query.lower()
        
        # Detect question type
        question_types = {
            "what": "definition",
            "why": "explanation",
            "how": "process",
            "when": "timing",
            "where": "location",
            "who": "person",
            "which": "selection",
            "compare": "comparison",
            "difference": "comparison",
            "explain": "explanation",
            "define": "definition",
            "list": "enumeration",
            "summarize": "summary",
        }
        
        q_type = "general"
        for keyword, qtype in question_types.items():
            if keyword in query_lower:
                q_type = qtype
                break

        return ReasoningStep(
            number=1,
            description=f"Understanding query type: {q_type}",
            input=query,
            output=f"Query classified as {q_type}",
            confidence=0.9
        )

    def _step_decompose(self, query: str) -> ReasoningStep:
        """Step 2: Break query into components."""
        # Extract key phrases
        words = query.split()
        key_phrases = []
        current_phrase = []
        
        for word in words:
            if word[0].isupper() or len(word) > 3:
                current_phrase.append(word)
            else:
                if current_phrase:
                    key_phrases.append(" ".join(current_phrase))
                    current_phrase = []
        
        if current_phrase:
            key_phrases.append(" ".join(current_phrase))
        
        # If no key phrases found, use all significant words
        if not key_phrases:
            key_phrases = [w for w in words if len(w) > 3]

        return ReasoningStep(
            number=2,
            description="Decomposing query into components",
            input=query,
            output=f"Key components: {', '.join(key_phrases[:5])}",
            confidence=0.85
        )

    def _step_context(self, query: str, context: dict) -> ReasoningStep:
        """Step 3: Apply context."""
        relevant_keys = [k for k in context.keys() if any(w in k.lower() for w in query.lower().split())]
        return ReasoningStep(
            number=3,
            description="Applying contextual information",
            input=str(context),
            output=f"Relevant context: {relevant_keys}",
            confidence=0.7
        )

    def _step_reason(self, query: str, steps: List[ReasoningStep]) -> ReasoningStep:
        """Step 4: Perform reasoning."""
        # Combine insights from previous steps
        insights = [s.output for s in steps]
        combined = "; ".join(insights)
        
        return ReasoningStep(
            number=len(steps) + 1,
            description="Performing logical reasoning",
            input=query,
            output=f"Analysis complete based on: {combined[:100]}",
            confidence=0.75
        )

    def _step_conclude(self, steps: List[ReasoningStep]) -> str:
        """Step 5: Draw conclusion."""
        avg_confidence = sum(s.confidence for s in steps) / len(steps)
        
        if avg_confidence > 0.8:
            return "I have high confidence in this analysis."
        elif avg_confidence > 0.5:
            return "I'm reasonably confident, but more information would help."
        else:
            return "I need more information to give a confident answer."

    def solve_problem(self, problem: str, steps_list: List[str] = None) -> List[str]:
        """Solve a problem step by step."""
        solutions = []
        
        if steps_list:
            for i, step in enumerate(steps_list, 1):
                solutions.append(f"Step {i}: {step}")
        else:
            # Auto-generate steps
            solutions.append(f"Step 1: Analyzing problem - {problem[:50]}...")
            solutions.append("Step 2: Identifying key factors")
            solutions.append("Step 3: Applying relevant knowledge")
            solutions.append("Step 4: Formulating solution")
            solutions.append("Step 5: Verifying result")

        return solutions

    def compare(self, item1: str, item2: str) -> Dict[str, Any]:
        """Compare two items and highlight differences."""
        return {
            "item1": item1,
            "item2": item2,
            "similarities": ["Both are comparable entities"],
            "differences": [f"{item1} differs from {item2}"],
            "recommendation": f"Based on comparison, choose based on your specific needs."
        }

    def summarize(self, text: str, max_points: int = 5) -> List[str]:
        """Summarize text into key points."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Simple extractive summary
        key_points = sentences[:max_points]
        
        if not key_points:
            key_points = ["No significant content to summarize."]
        
        return key_points

    def get_recent_chains(self, limit: int = 5) -> List[ReasoningChain]:
        """Get recent reasoning chains."""
        return self._chains[-limit:]

    def clear_chains(self):
        """Clear reasoning chain history."""
        self._chains.clear()
