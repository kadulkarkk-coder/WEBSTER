"""
WEBSTER Browser Controller
===========================
Opens URLs, searches web, controls browser tabs.
"""

import webbrowser
import subprocess
import os
from typing import List, Optional, Dict
from webster.core.logger import Logger


class BrowserController:
    """Control web browser - open URLs, search, manage tabs."""

    def __init__(self):
        self.logger = Logger().get_logger("BROWSER")
        self._browser_paths = {
            "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            "firefox": "C:/Program Files/Mozilla Firefox/firefox.exe",
        }

    def open(self, url: str) -> bool:
        """Open URL in default browser."""
        webbrowser.open(url)
        self.logger.info(f"Opened: {url}")
        return True

    def open_new_tab(self, url: str) -> bool:
        """Open URL in new tab."""
        webbrowser.open_new_tab(url)
        return True

    def search(self, query: str, engine: str = "google") -> bool:
        """Search the web."""
        engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
            "yahoo": "https://search.yahoo.com/search?p=",
        }
        base = engines.get(engine, engines["google"])
        self.open(base + query.replace(" ", "+"))
        return True

    def open_chrome(self, url: str = "") -> bool:
        """Open URL in Chrome."""
        path = self._browser_paths.get("chrome", "chrome")
        try:
            subprocess.Popen([path, url], shell=True)
            return True
        except:
            return self.open(url)

    def open_incognito(self, url: str = "") -> bool:
        """Open URL in incognito/private mode."""
        try:
            path = self._browser_paths.get("chrome", "chrome")
            subprocess.Popen([path, "--incognito", url], shell=True)
            return True
        except:
            self.logger.warning("Incognito mode failed, opening normally")
            return self.open(url)
