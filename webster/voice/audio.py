"""
WEBSTER Audio Utilities
=======================
Audio capture, playback, and processing utilities.
"""

import os
import wave
import tempfile
import threading
from typing import Optional
from pathlib import Path

from webster.core.logger import Logger


class AudioUtils:
    """Audio capture, playback, and file management."""

    def __init__(self):
        self.logger = Logger().get_logger("AUDIO")
        self._recording = False
        self._frames = []

    def record(self, duration: float = 5.0, sample_rate: int = 16000) -> Optional[bytes]:
        """Record audio for a specified duration."""
        try:
            import sounddevice as sd
            self._recording = True
            self.logger.info(f"Recording for {duration}s...")
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()
            self._recording = False
            return recording.tobytes()
        except Exception as e:
            self.logger.error(f"Recording failed: {e}")
            return None

    def record_stream(self, callback, sample_rate: int = 16000):
        """Record streaming audio with callback."""
        try:
            import sounddevice as sd
            def stream_callback(indata, frames, time_info, status):
                callback(indata.copy())

            stream = sd.InputStream(samplerate=sample_rate, channels=1, callback=stream_callback)
            stream.start()
            return stream
        except Exception as e:
            self.logger.error(f"Stream failed: {e}")
            return None

    def save_wav(self, data: bytes, filepath: str, sample_rate: int = 16000):
        """Save audio data as WAV file."""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with wave.open(filepath, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(data)
            return True
        except Exception as e:
            self.logger.error(f"Save WAV failed: {e}")
            return False

    def play(self, filepath: str):
        """Play an audio file."""
        try:
            import playsound
            playsound.playsound(filepath)
        except Exception as e:
            self.logger.error(f"Playback failed: {e}")

    def play_async(self, filepath: str):
        """Play audio in background."""
        thread = threading.Thread(target=self.play, args=(filepath,), daemon=True)
        thread.start()

    def get_audio_devices(self) -> list:
        """List available audio devices."""
        try:
            import sounddevice as sd
            devices = []
            for i, dev in enumerate(sd.query_devices()):
                devices.append({
                    "index": i, "name": dev["name"],
                    "channels": dev["max_input_channels"],
                    "sample_rate": dev["default_samplerate"],
                })
            return devices
        except:
            return []

    @staticmethod
    def create_silence(duration_sec: float, sample_rate: int = 16000) -> bytes:
        """Create silence audio data."""
        import numpy as np
        return np.zeros(int(duration_sec * sample_rate), dtype=np.int16).tobytes()
