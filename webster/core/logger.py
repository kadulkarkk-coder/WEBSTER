"""
WEBSTER Logger
==============
Centralized logging with file rotation and console output.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Application-wide logger with structured output."""

    _instance = None
    _loggers: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._level = logging.DEBUG
        self._setup()

    def _setup(self):
        """Configure logging system."""
        log_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) / "webster" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{today}.log"

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        self._file_handler = file_handler
        self._console_handler = console_handler

    def get_logger(self, name: str = "WEBSTER") -> logging.Logger:
        """Get or create a named logger."""
        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        if not logger.handlers:
            logger.addHandler(self._file_handler)
            logger.addHandler(self._console_handler)

        self._loggers[name] = logger
        return logger

    def info(self, message: str, name: str = "WEBSTER"):
        self.get_logger(name).info(message)

    def debug(self, message: str, name: str = "WEBSTER"):
        self.get_logger(name).debug(message)

    def warning(self, message: str, name: str = "WEBSTER"):
        self.get_logger(name).warning(message)

    def error(self, message: str, name: str = "WEBSTER"):
        self.get_logger(name).error(message)

    def critical(self, message: str, name: str = "WEBSTER"):
        self.get_logger(name).critical(message)

    def exception(self, message: str, name: str = "WEBSTER"):
        self.get_logger(name).exception(message)

    def set_level(self, level: int):
        self._level = level
        for logger in self._loggers.values():
            logger.setLevel(level)
