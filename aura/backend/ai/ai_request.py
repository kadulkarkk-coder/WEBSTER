"""AI request data structures."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AIRequest:
    """
    ==================================================
                    AI Request
    ==================================================

    Standard request object passed into the AI engine.

    Every generator creates one of these.

    ==================================================
    """

    prompt: str

    system_prompt: str = ""

    model: str = "gemini-2.5-flash"

    temperature: float = 0.4

    max_tokens: int | None = None

    stream: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)