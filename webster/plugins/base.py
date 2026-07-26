"""
WEBSTER Plugin Base
===================
Base class for all WEBSTER plugins.
"""

from typing import Any, Dict, List, Optional
from webster.core.logger import Logger


class BasePlugin:
    """Base class that all plugins extend."""

    def __init__(self, name: str = "", version: str = "1.0.0", description: str = ""):
        self.name = name or self.__class__.__name__
        self.version = version
        self.description = description
        self._enabled = True
        self.logger = Logger().get_logger(f"PLUGIN_{self.name.upper()}")

    def on_load(self):
        """Called when plugin is loaded."""
        pass

    def on_unload(self):
        """Called when plugin is unloaded."""
        pass

    def on_enable(self):
        """Called when plugin is enabled."""
        self._enabled = True

    def on_disable(self):
        """Called when plugin is disabled."""
        self._enabled = False

    def execute(self, action: str, **kwargs) -> Any:
        """Execute a plugin action."""
        return None

    def get_manifest(self) -> Dict:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "enabled": self._enabled,
        }

    @property
    def is_enabled(self) -> bool:
        return self._enabled
