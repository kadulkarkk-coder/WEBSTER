"""
WEBSTER Path Configuration
==========================
Centralized path management for all application directories.
"""

import os
from pathlib import Path


class Paths:
    """Manages all file paths used by WEBSTER."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._root = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self._ensure_directories()

    def _ensure_directories(self):
        """Create all required directories."""
        dirs = [
            self.data,
            self.memory,
            self.logs,
            self.database,
            self.vector_store,
            self.plugins,
            self.assets_icons,
            self.assets_sounds,
            self.assets_wallpapers,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    @property
    def data(self) -> Path:
        return self._root / "data"

    @property
    def memory(self) -> Path:
        return self._root / "data" / "memory"

    @property
    def logs(self) -> Path:
        return self._root / "webster" / "logs"

    @property
    def database(self) -> Path:
        return self._root / "webster" / "database"

    @property
    def vector_store(self) -> Path:
        return self._root / "webster" / "database" / "vector_store"

    @property
    def plugins(self) -> Path:
        return self._root / "webster" / "plugins"

    @property
    def assets(self) -> Path:
        return self._root / "webster" / "assets"

    @property
    def assets_icons(self) -> Path:
        return self.assets / "icons"

    @property
    def assets_sounds(self) -> Path:
        return self.assets / "sounds"

    @property
    def assets_wallpapers(self) -> Path:
        return self.assets / "wallpapers"

    @property
    def dashboard_static(self) -> Path:
        return self._root / "webster" / "dashboard" / "static"

    @property
    def dashboard_templates(self) -> Path:
        return self._root / "webster" / "dashboard" / "templates"

    @property
    def mobile_static(self) -> Path:
        return self._root / "webster" / "mobile" / "static"

    @property
    def mobile_templates(self) -> Path:
        return self._root / "webster" / "mobile" / "templates"

    @property
    def config_file(self) -> Path:
        return self._root / "config" / "settings.json"

    @property
    def env_file(self) -> Path:
        return self._root / ".env"

    def resolve(self, *parts: str) -> Path:
        """Resolve path relative to root."""
        return self._root.joinpath(*parts)
