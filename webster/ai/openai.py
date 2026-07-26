"""
WEBSTER OpenAI Provider
=======================
OpenAI API integration (GPT-4, GPT-3.5).
"""

import os
from typing import Generator

from webster.ai.base import BaseProvider
from webster.core.logger import Logger


class OpenAIProvider(BaseProvider):
    """OpenAI API provider."""

    def __init__(self):
        self.logger = Logger().get_logger("OPENAI")
        self.client = None
        self.model = "gpt-3.5-turbo"
        self._available = False

    def initialize(self):
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY", "")
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
                self._available = True
                self.logger.info(f"OpenAI connected ({self.model})")
        except Exception as e:
            self.logger.warning(f"OpenAI not available: {e}")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self._available:
            return "[OpenAI not configured]"
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 4096),
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[OpenAI error: {e}]"

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        if not self._available:
            yield "[OpenAI not configured]"
            return
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"[OpenAI error: {e}]"

    def get_name(self) -> str:
        return "OpenAI"

    def is_available(self) -> bool:
        return self._available
