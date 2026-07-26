"""
WEBSTER Web Dashboard
=====================
FastAPI-based web dashboard for WEBSTER system monitoring and control.
Lazy imports to avoid Python 3.14 compatibility issues.
"""

import logging
import threading
from pathlib import Path
from typing import Optional

logger = logging.getLogger("webster.dashboard")


class DashboardServer:
    """FastAPI web dashboard server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.app = None
        self._running = False
        self._thread = None

    def _init_app(self):
        """Initialize FastAPI app with lazy imports."""
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import HTMLResponse
        import json

        self.app = FastAPI(title="WEBSTER Dashboard")

        static_dir = Path(__file__).parent / "static"
        templates_dir = Path(__file__).parent / "templates"

        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

        @self.app.get("/")
        async def index():
            index_file = templates_dir / "index.html"
            if index_file.exists():
                content = index_file.read_text(encoding="utf-8")
                return HTMLResponse(content)
            return {"status": "WEBSTER Dashboard", "message": "Template not found"}

        @self.app.get("/api/status")
        async def api_status():
            return {
                "app": "WEBSTER", "version": "0.1.0",
                "ai": "Spidey", "status": "online",
                "conversations": 0, "memory_items": 0,
                "study_items": 0, "automations": 0,
                "provider": "Gemini"
            }

        @self.app.get("/api/health")
        async def health():
            return {"status": "healthy", "service": "WEBSTER"}

        @self.app.post("/api/command")
        async def execute_command(command: dict):
            cmd = command.get("command", "")
            return {"status": "received", "command": cmd}

    def start(self):
        """Start the dashboard server (blocking)."""
        self._init_app()
        import uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

    def start_background(self):
        """Start the server in a background thread."""
        if self._running:
            return None
        self._running = True
        self._thread = threading.Thread(target=self.start, daemon=True)
        self._thread.start()
        logger.info(f"Dashboard started on http://{self.host}:{self.port}")
        return self._thread

    def stop(self):
        """Stop the server."""
        self._running = False
