"""
WEBSTER Mobile Server
=====================
Lightweight FastAPI server serving mobile-optimized web interface.
"""

import threading
from typing import Optional
from webster.core.logger import Logger


class MobileServer:
    """Web server for mobile companion access."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8766):
        self.logger = Logger().get_logger("MOBILE")
        self.host = host
        self.port = port
        self._thread = None
        self._running = False

    def start(self):
        if self._running:
            return
        try:
            import uvicorn
            from fastapi import FastAPI
            app = FastAPI(title="WEBSTER Mobile")

            @app.get("/")
            def index():
                return {"message": "WEBSTER Mobile API"}

            @app.get("/health")
            def health():
                return {"status": "ok"}

            self._thread = threading.Thread(
                target=lambda: uvicorn.run(app, host=self.host, port=self.port, log_level="error"),
                daemon=True
            )
            self._thread.start()
            self._running = True
            self.logger.info(f"Mobile server on http://{self.host}:{self.port}")
        except ImportError:
            self.logger.warning("FastAPI not installed, mobile unavailable")

    def stop(self):
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"
