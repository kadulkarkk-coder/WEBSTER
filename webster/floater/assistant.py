"""
WEBSTER Floating Assistant
===========================
Quick-access floating assistant window (always-on-top).
"""

from typing import Any, Callable, Dict, Optional
from webster.core.logger import Logger
from webster.floater.orb import SpideyOrb


class FloatingAssistant:
    """
    Always-on-top mini assistant that provides quick access to Spidey.
    Features: push-to-talk, quick commands, drag & drop files.
    """

    def __init__(self):
        self.logger = Logger().get_logger("FLOAT_ASST")
        self.orb = SpideyOrb()
        self._visible = False
        self._on_query: Optional[Callable] = None
        self.logger.info("Floating assistant initialized")

    def set_query_handler(self, handler: Callable):
        self._on_query = handler

    def send_query(self, query: str):
        if self._on_query:
            self._on_query(query)

    def show(self):
        self._visible = True
        self.orb.show()

    def hide(self):
        self._visible = False
        self.orb.hide()

    def toggle(self):
        if self._visible:
            self.hide()
        else:
            self.show()

    def start_listening(self):
        self.orb.set_status("listening")

    def stop_listening(self):
        self.orb.set_status("idle")

    def show_thinking(self):
        self.orb.set_status("thinking")

    def show_speaking(self):
        self.orb.set_status("speaking")

    def show_error(self):
        self.orb.set_status("error")

    @property
    def is_visible(self) -> bool:
        return self._visible
