"""AI response data structures."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AIResponse:
    """
    ==================================================
                    AI Response
    ==================================================

    Returned by AIEngine.generate().

    ==================================================
    """

    success: bool

    text: str = ""

    error: str = ""

    model: str = ""

    latency: float = 0.0

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    metadata: dict[str, Any] = field(default_factory=dict)
    