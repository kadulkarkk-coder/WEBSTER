"""
WEBSTER Voice Controller
=========================
Central controller for all voice operations (STT, TTS, wake word).
"""

from typing import Optional, Callable
from webster.core.logger import Logger
from webster.voice.listen import SpeechRecognizer
from webster.voice.speak import TextToSpeech
from webster.voice.wakeword import WakeWordDetector


class VoiceController:
    """
    Central voice controller managing:
    - Speech-to-text (listening)
    - Text-to-speech (speaking)
    - Wake word detection ("Hey Spidey")
    """

    def __init__(self):
        self.logger = Logger().get_logger("VOICE_CTRL")
        self.speech = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.wake = WakeWordDetector()
        self._enabled = False
        self._wake_callback: Optional[Callable] = None
        self.logger.info("Voice controller initialized")

    def enable(self):
        self._enabled = True
        self.logger.info("Voice enabled")

    def disable(self):
        self._enabled = False
        self.wake.stop_listening()
        self.logger.info("Voice disabled")

    def speak(self, text: str) -> bool:
        if not self._enabled:
            return False
        return self.tts.speak(text)

    def speak_async(self, text: str):
        if self._enabled:
            self.tts.speak_async(text)

    def listen(self, timeout: float = 5.0) -> Optional[str]:
        if not self._enabled:
            return None
        return self.speech.listen(timeout=timeout)

    def start_wake_word(self, callback: Optional[Callable] = None):
        if callback:
            self._wake_callback = callback
        if self._wake_callback:
            self.wake.set_callback(self._wake_callback)
        self.wake.start_listening()

    def stop_wake_word(self):
        self.wake.stop_listening()

    def set_voice(self, voice: str):
        self.tts.set_voice(voice)

    def set_speech_rate(self, rate: int):
        self.tts.set_rate(rate)

    def set_volume(self, volume: float):
        self.tts.set_volume(volume)

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def is_listening(self) -> bool:
        return self.speech.is_listening

    @property
    def is_speaking(self) -> bool:
        return self.tts.is_speaking

    @property
    def is_wake_listening(self) -> bool:
        return self.wake.is_listening

    def status(self) -> dict:
        return {
            "enabled": self._enabled,
            "stt_available": self.speech.is_available,
            "tts_available": self.tts.is_available,
            "wake_available": self.wake.is_available,
            "listening": self.is_listening,
            "speaking": self.is_speaking,
            "wake_listening": self.is_wake_listening,
        }

    def shutdown(self):
        self.disable()
        self.logger.info("Voice controller shut down")
