"""
WEBSTER Text-to-Speech
======================
Lazy-loading TTS to avoid Python 3.14 dependency crashes.
"""

from typing import Optional
from webster.core.logger import Logger


class TextToSpeech:
    """
    Converts text to speech using available engine.
    Uses lazy imports to avoid Python 3.14 compatibility issues.
    """

    def __init__(self):
        self.logger = Logger().get_logger("TTS")
        self._engine = None
        self._available = False
        self._speaking = False
        self._voice = None
        self._rate = 180
        self._volume = 0.8

    def _ensure_engine(self):
        """Try to load TTS engine (lazy)."""
        if self._engine is not None:
            return
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._available = True
            self.logger.info("pyttsx3 TTS loaded")
        except ImportError:
            self.logger.warning("pyttsx3 not available")
        except Exception as e:
            self.logger.warning(f"TTS not available: {e}")

    def speak(self, text: str) -> bool:
        """Speak text synchronously."""
        self._ensure_engine()
        if not self._available or not self._engine:
            print(f"[TTS] {text}")
            return False
        try:
            self._speaking = True
            self._engine.say(text)
            self._engine.runAndWait()
            self._speaking = False
            return True
        except Exception as e:
            self.logger.error(f"Speak error: {e}")
            self._speaking = False
            return False

    def speak_async(self, text: str):
        """Speak text asynchronously."""
        import threading
        thread = threading.Thread(target=self.speak, args=(text,), daemon=True)
        thread.start()

    def set_voice(self, voice: str):
        self._voice = voice

    def set_rate(self, rate: int):
        self._rate = rate
        self._ensure_engine()
        if self._engine:
            self._engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        self._volume = volume
        self._ensure_engine()
        if self._engine:
            self._engine.setProperty('volume', volume)

    @property
    def is_speaking(self) -> bool:
        return self._speaking

    @property
    def is_available(self) -> bool:
        self._ensure_engine()
        return self._available

    def shutdown(self):
        self._engine = None
        self._available = False
