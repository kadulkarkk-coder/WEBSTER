"""
WEBSTER Base AI Provider
========================
Abstract base class for all AI providers (Gemini, OpenAI, Ollama).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Generator


class BaseProvider(ABC):
    """Abstract base for AI providers."""

    @abstractmethod
    def initialize(self):
        """Initialize the provider (load API key, create client)."""
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from a prompt."""
        pass

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Generate a streaming response."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get provider name."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available/configured."""
        pass

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Chat with message history (optional override)."""
        prompt = self._messages_to_prompt(messages)
        return self.generate(prompt, **kwargs)

    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert message list to a single prompt string."""
        parts = []
        for msg in messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            parts.append(f"{role}: {content}")
        parts.append("ASSISTANT:")
        return "\n".join(parts)

    def shutdown(self):
        """Cleanup provider resources."""
        pass

    def get_status(self) -> str:
        """Get provider status string."""
        return "Online" if self.is_available() else "Offline"
