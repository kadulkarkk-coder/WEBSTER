"""
WEBSTER Speech-to-Text
======================
Lazy-loading speech recognition to avoid Python 3.14 hashlib crash.
"""

import os
import tempfile
from typing import Optional, Callable
from webster.core.logger import Logger
from webster.core.errors import VoiceError


class SpeechRecognizer:
    """
    Captures audio from microphone and converts to text.
    Uses lazy imports to avoid Python 3.14 compatibility issues.
    """

    def __init__(self):
        self.logger = Logger().get_logger("STT")
        self._model = None
        self._available = False
        self._listening = False
        self._recognizer = None

    def _ensure_engine(self):
        """Try to load speech recognition (lazy)."""
        if self._recognizer is not None:
            return
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._available = True
            self.logger.info("SpeechRecognition loaded")
        except ImportError:
            self.logger.warning("No speech recognition available")
        except Exception as e:
            self.logger.warning(f"Speech recognition not available: {e}")

    def listen(self, timeout: float = 5.0, phrase_time_limit: float = None) -> Optional[str]:
        """Listen for speech and return transcribed text."""
        self._ensure_engine()
        if not self._available or not self._recognizer:
            return None

        try:
            import speech_recognition as sr
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self._listening = True
                audio = self._recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
                self._listening = False
            return self._recognizer.recognize_google(audio)
        except ImportError:
            return None
        except Exception as e:
            self.logger.debug(f"Listen error: {e}")
            return None
        finally:
            self._listening = False

    def stop_listening(self):
        self._listening = False

    @property
    def is_listening(self) -> bool:
        return self._listening

    @property
    def is_available(self) -> bool:
        self._ensure_engine()
        return self._available
