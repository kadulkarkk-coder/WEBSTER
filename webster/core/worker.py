"""
WEBSTER Background Worker
=========================
Manages background threads for async operations.
"""

import threading
import queue
import time
import traceback
from typing import Any, Callable, Optional
from enum import Enum

from webster.core.logger import Logger


class WorkerState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"


class BackgroundWorker:
    """
    Background thread worker for async task execution.
    Streams results back via queue for UI updates.
    """

    END = object()

    def __init__(self, name: str = "Worker"):
        self.logger = Logger().get_logger(name)
        self.name = name
        self._thread: Optional[threading.Thread] = None
        self._queue: queue.Queue = queue.Queue()
        self._state = WorkerState.IDLE

    def start_stream(self, target: Callable, *args, **kwargs):
        """Start a streaming task in background thread."""
        if self._state == WorkerState.RUNNING:
            self.logger.warning("Worker already running")
            return

        self._state = WorkerState.RUNNING
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

        self._thread = threading.Thread(
            target=self._run_stream,
            args=(target, args, kwargs),
            daemon=True
        )
        self._thread.start()

    def _run_stream(self, target: Callable, args: tuple, kwargs: dict):
        try:
            for chunk in target(*args, **kwargs):
                self._queue.put(chunk)
            self._state = WorkerState.IDLE
        except Exception as e:
            traceback.print_exc()
            self._queue.put(e)
            self._state = WorkerState.ERROR
        finally:
            self._queue.put(self.END)

    def get_chunk(self) -> Any:
        """Get next chunk from queue (non-blocking)."""
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def wait_for_result(self, timeout: float = 30.0) -> Any:
        """Wait for and return the final result."""
        result = []
        start = time.time()
        while time.time() - start < timeout:
            chunk = self.get_chunk()
            if chunk is self.END:
                break
            elif chunk is not None:
                result.append(chunk)
            time.sleep(0.05)
        return "".join(str(r) for r in result) if result else None

    def execute(self, target: Callable, *args, **kwargs):
        """Execute a function in background thread."""
        self._thread = threading.Thread(
            target=self._run,
            args=(target, args, kwargs),
            daemon=True
        )
        self._thread.start()

    def _run(self, target: Callable, args: tuple, kwargs: dict):
        try:
            target(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Worker task failed: {e}")

    @property
    def is_running(self) -> bool:
        return self._state == WorkerState.RUNNING

    @property
    def state(self) -> WorkerState:
        return self._state

    def join(self, timeout: float = 5.0):
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)

    def stop(self):
        self._state = WorkerState.STOPPED
        self.join()

    def reset(self):
        self._state = WorkerState.IDLE
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
