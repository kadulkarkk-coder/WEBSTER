"""
WEBSTER Ollama AI Provider
==========================
Local LLM inference via Ollama API.
Uses raw http.client to avoid Python 3.14 urllib/_zstd issues.
"""

import json
import socket
from typing import Generator
from http.client import HTTPConnection

from webster.ai.base import BaseProvider
from webster.core.logger import Logger


class OllamaProvider(BaseProvider):
    """Ollama local LLM provider."""

    def __init__(self):
        self.logger = Logger().get_logger("OLLAMA")
        self.host = "localhost"
        self.port = 11434
        self.model = "llama3.2"
        self._available = False

    def _request(self, method: str, path: str, body: bytes = None) -> tuple:
        """Make HTTP request to Ollama API."""
        conn = HTTPConnection(self.host, self.port, timeout=30)
        try:
            headers = {"Content-Type": "application/json"}
            conn.request(method, path, body=body, headers=headers)
            response = conn.getresponse()
            data = response.read()
            return response.status, data
        finally:
            conn.close()

    def initialize(self):
        try:
            status, data = self._request("GET", "/api/tags")
            if status == 200:
                result = json.loads(data.decode())
                models = result.get("models", [])
                if models:
                    self.model = models[0]["name"]
                self._available = True
                self.logger.info(f"Ollama connected ({self.model})")
        except (ConnectionRefusedError, socket.error, TimeoutError, Exception) as e:
            self._available = False
            self.logger.warning(f"Ollama not available: {e}")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self._available:
            return "[Ollama not available]"
        try:
            payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False})
            status, data = self._request("POST", "/api/generate", body=payload.encode())
            if status == 200:
                result = json.loads(data.decode())
                return result.get("response", "")
            return f"[Ollama error: {status}]"
        except Exception as e:
            return f"[Ollama error: {e}]"

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        if not self._available:
            yield "[Ollama not available]"
            return
        try:
            payload = json.dumps({"model": self.model, "prompt": prompt, "stream": True})
            conn = HTTPConnection(self.host, self.port, timeout=120)
            conn.request("POST", "/api/generate", body=payload.encode(),
                         headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            while True:
                line = response.readline()
                if not line:
                    break
                try:
                    data = json.loads(line.decode().strip())
                    if data.get("done"):
                        break
                    yield data.get("response", "")
                except (json.JSONDecodeError, ValueError):
                    continue
            conn.close()
        except Exception as e:
            yield f"[Ollama error: {e}]"

    def get_name(self) -> str:
        return "Ollama"

    def is_available(self) -> bool:
        return self._available
