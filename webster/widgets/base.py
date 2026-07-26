"""
WEBSTER Widget Base
===================
Base class for all desktop widgets.
"""

from typing import Any, Dict, Optional
from webster.core.logger import Logger


class BaseWidget:
    """Base widget class that all widgets extend."""

    def __init__(self, name: str, title: str, width: int = 300, height: int = 200):
        self.name = name
        self.title = title
        self.width = width
        self.height = height
        self._x = 100
        self._y = 100
        self._visible = True
        self._data: Dict = {}
        self.logger = Logger().get_logger(f"WIDGET_{name.upper()}")

    def build(self):
        """Build the widget UI. Override in subclass."""
        pass

    def update(self, data: Optional[Dict] = None):
        """Update widget with new data."""
        if data:
            self._data.update(data)

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def move(self, x: int, y: int):
        self._x = x
        self._y = y

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height

    def get_state(self) -> Dict:
        return {
            "name": self.name,
            "title": self.title,
            "x": self._x,
            "y": self._y,
            "width": self.width,
            "height": self.height,
            "visible": self._visible,
            "data": self._data,
        }

    @property
    def is_visible(self) -> bool:
        return self._visible
