"""
WEBSTER Widget Manager
=====================
Manages all desktop widgets - create, show, hide, arrange.
"""

from typing import Any, Dict, List, Optional
from webster.core.logger import Logger
from webster.widgets.base import BaseWidget


class WidgetManager:
    """Manage multiple widgets: register, position, visibility."""

    def __init__(self):
        self.logger = Logger().get_logger("WIDGET_MGR")
        self._widgets: Dict[str, BaseWidget] = {}

    def register(self, widget: BaseWidget):
        self._widgets[widget.name] = widget
        self.logger.info(f"Widget registered: {widget.name}")

    def get(self, name: str) -> Optional[BaseWidget]:
        return self._widgets.get(name)

    def show_all(self):
        for widget in self._widgets.values():
            widget.show()

    def hide_all(self):
        for widget in self._widgets.values():
            widget.hide()

    def list_widgets(self) -> List[Dict]:
        return [w.get_state() for w in self._widgets.values()]

    def remove(self, name: str) -> bool:
        if name in self._widgets:
            del self._widgets[name]
            return True
        return False

    def count(self) -> int:
        return len(self._widgets)

    def get_all_states(self) -> Dict[str, Dict]:
        return {n: w.get_state() for n, w in self._widgets.items()}
