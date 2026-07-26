"""
WEBSTER Wake Word Detector
==========================
Detects "Hey Spidey" wake word using audio processing.
"""

import os
import re
import threading
from typing import Optional, Callable

from webster.core.logger import Logger


class WakeWordDetector:
    """
    Listens for "Hey Spidey" or "Spidey" wake word in the background.
    Uses Vosk speech recognition for offline wake word detection.
    """

    WAKE_WORDS = ["hey spidey", "spidey", "hey spider", "spider"]

    def __init__(self):
        self.logger = Logger().get_logger("WAKE_WORD")
        self._model = None
        self._recognizer = None
        self._available = False
        self._listening = False
        self._callback: Optional[Callable] = None
        self._init_model()

    def _init_model(self):
        try:
            import vosk
            import json
            model_path = os.getenv("VOSK_MODEL_PATH", "models/vosk-model-small-en-us-0.15")
            if os.path.exists(model_path):
                self._model = vosk.Model(model_path)
                self._available = True
                self.logger.info("Vosk model loaded for wake word")
        except ImportError:
            self.logger.info("Vosk not available, using simple keyword detection")
            self._available = True

    def set_callback(self, callback: Callable):
        self._callback = callback

    def start_listening(self):
        if self._listening or not self._available:
            return
        self._listening = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()
        self.logger.info("Wake word listening started")

    def stop_listening(self):
        self._listening = False

    def _listen_loop(self):
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                while self._listening:
                    try:
                        audio = r.listen(source, timeout=1.0, phrase_time_limit=3)
                        try:
                            text = r.recognize_google(audio).lower()
                            if self._detect_wake_word(text):
                                self._on_wake_detected(text)
                        except:
                            pass
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        self.logger.error(f"Wake word loop error: {e}")
        except Exception as e:
            self.logger.error(f"Microphone not available: {e}")

    def _detect_wake_word(self, text: str) -> bool:
        text = text.lower().strip()
        for word in self.WAKE_WORDS:
            if word in text or text == word:
                return True
        return False

    def _on_wake_detected(self, text: str):
        self.logger.info(f"Wake word detected: {text}")
        if self._callback:
            threading.Thread(target=self._callback, args=(text,), daemon=True).start()

    @property
    def is_listening(self) -> bool:
        return self._listening

    @property
    def is_available(self) -> bool:
        return self._available
