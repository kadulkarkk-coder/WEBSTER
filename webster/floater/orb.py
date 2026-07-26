"""
WEBSTER Spidey Orb
==================
Floating circular UI element that represents Spidey availability.
"""

from webster.core.logger import Logger


class SpideyOrb:
    """
    Floating orb that shows Spidey's status:
    - Idle (dim)
    - Listening (pulsing)
    - Thinking (spinning)
    - Speaking (glowing)
    """

    STATUS_COLORS = {
        "idle": "#555555",
        "listening": "#00e5ff",
        "thinking": "#7c4dff",
        "speaking": "#00e676",
        "error": "#ff1744",
        "processing": "#ff9100",
    }

    def __init__(self):
        self.logger = Logger().get_logger("ORB")
        self._status = "idle"
        self._x = 50
        self._y = 50
        self._size = 60
        self._visible = False

    def set_status(self, status: str):
        if status in self.STATUS_COLORS:
            self._status = status
            self.logger.debug(f"Orb status: {status}")

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def move(self, x: int, y: int):
        self._x = x
        self._y = y

    def resize(self, size: int):
        self._size = size

    def get_color(self) -> str:
        return self.STATUS_COLORS.get(self._status, "#555555")

    @property
    def status(self) -> str:
        return self._status

    @property
    def is_visible(self) -> bool:
        return self._visible
