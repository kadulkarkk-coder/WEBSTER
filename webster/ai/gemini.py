"""
WEBSTER Gemini AI Provider
==========================
Google Gemini integration with streaming, chat history, and error handling.
"""

import os
import time
import random
import traceback
from typing import Any, Dict, Generator, List, Optional

from webster.ai.base import BaseProvider
from webster.core.logger import Logger
from webster.core.errors import APIKeyError, QuotaExceededError, RateLimitError


class GeminiProvider(BaseProvider):
    """Google Gemini AI provider."""

    def __init__(self):
        self.logger = Logger().get_logger("GEMINI")
        self.client = None
        self.model = "gemini-2.0-flash"
        self._available = False
        self._last_error: Optional[str] = None
        self.max_retries = 3
        self.retry_delay = 1

    def initialize(self):
        """Initialize Gemini client."""
        try:
            from google import genai
            api_key = os.getenv("GEMINI_API_KEY", "")
            if not api_key:
                from config.api_keys import APIKeys
                api_key = APIKeys.get("gemini", "")
            if not api_key:
                raise APIKeyError("Gemini API key not found")
            self.client = genai.Client(api_key=api_key)
            self._available = True
            self.logger.info(f"Gemini connected ({self.model})")
        except Exception as e:
            self._available = False
            self._last_error = str(e)
            self.logger.error(f"Gemini init failed: {e}")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text response."""
        if not self._available:
            return "[Gemini not configured]"
        retry_count = 0
        while retry_count <= self.max_retries:
            try:
                response = self.client.models.generate_content(
                    model=self.model, contents=prompt
                )
                self._last_error = None
                return response.text
            except Exception as e:
                if not self._should_retry(e):
                    raise
                retry_count += 1
                if retry_count > self.max_retries:
                    raise
                delay = self.retry_delay * (2 ** (retry_count - 1)) + random.uniform(0, 0.5)
                time.sleep(delay)

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Stream text response."""
        if not self._available:
            yield "[Gemini not configured]"
            return
        retry_count = 0
        while retry_count <= self.max_retries:
            try:
                response = self.client.models.generate_content_stream(
                    model=self.model, contents=prompt
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
                return
            except Exception as e:
                if not self._should_retry(e):
                    raise
                retry_count += 1
                if retry_count > self.max_retries:
                    raise
                delay = self.retry_delay * (2 ** (retry_count - 1)) + random.uniform(0, 0.5)
                time.sleep(delay)

    def _should_retry(self, error: Exception) -> bool:
        text = str(error).upper()
        retryable = ["RESOURCE_EXHAUSTED", "429", "503", "UNAVAILABLE", "INTERNAL", "DEADLINE_EXCEEDED"]
        return any(item in text for item in retryable)

    def get_name(self) -> str:
        return "Gemini"

    def is_available(self) -> bool:
        return self._available

    def health(self) -> dict:
        return {
            "provider": "Gemini",
            "available": self._available,
            "model": self.model,
            "last_error": self._last_error,
        }

    def shutdown(self):
        self._available = False
        self.client = None
        self.logger.info("Gemini shutdown")
