"""
WEBSTER Provider Manager
=========================
Manages multiple AI providers and failover between them.
"""

from typing import Dict, List, Optional, Type

from webster.core.logger import Logger
from webster.ai.base import BaseProvider
from webster.ai.gemini import GeminiProvider
from webster.ai.ollama import OllamaProvider
from webster.ai.openai import OpenAIProvider


class ProviderManager:
    """
    Manages AI provider registration, activation, and failover.
    
    Priority order: Gemini > OpenAI > Ollama
    """

    def __init__(self):
        self.logger = Logger().get_logger("PROVIDER_MGR")
        self._providers: Dict[str, BaseProvider] = {}
        self._active: Optional[str] = None
        self._load_defaults()

    def _load_defaults(self):
        """Load default providers."""
        for provider_class in [GeminiProvider, OpenAIProvider, OllamaProvider]:
            try:
                name = provider_class().get_name().lower()
                self._providers[name] = provider_class
            except Exception:
                pass

    def register(self, name: str, provider: BaseProvider):
        self._providers[name.lower()] = provider
        self.logger.info(f"Registered provider: {name}")

    def activate(self, name: str) -> bool:
        name = name.lower()
        provider_class = self._providers.get(name)
        if not provider_class:
            self.logger.error(f"Provider not found: {name}")
            return False
        try:
            if callable(provider_class):
                provider = provider_class()
            else:
                provider = provider_class
            provider.initialize()
            self._providers[name] = provider
            self._active = name
            self.logger.info(f"Activated provider: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to activate {name}: {e}")
            return False

    def get_current(self) -> Optional[BaseProvider]:
        if self._active and self._active in self._providers:
            provider = self._providers[self._active]
            if not callable(provider):
                return provider
        return None

    def get_current_name(self) -> str:
        return self._active or "None"

    def list_providers(self) -> List[str]:
        names = []
        for name, provider in self._providers.items():
            if not callable(provider):
                names.append(name)
            else:
                names.append(f"{name} (not initialized)")
        return names

    def switch(self, name: str) -> bool:
        """Switch to a different provider with failover."""
        if self.activate(name):
            return True
        return self.failover()

    def failover(self) -> bool:
        """Try next available provider."""
        for name in ["gemini", "openai", "ollama"]:
            if name != self._active and name in self._providers:
                if self.activate(name):
                    self.logger.info(f"Failover to: {name}")
                    return True
        self.logger.error("No available provider for failover")
        return False

    def shutdown_all(self):
        for provider in self._providers.values():
            if hasattr(provider, "shutdown"):
                try:
                    provider.shutdown()
                except:
                    pass
        self.logger.info("All providers shut down")
