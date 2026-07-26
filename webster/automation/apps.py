"""
WEBSTER App Launcher
====================
Launch and manage applications on the system.
"""

import os
import subprocess
from typing import Dict, List, Optional
from webster.core.logger import Logger


class AppLauncher:
    """Launch system applications by name or path."""

    COMMON_APPS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "explorer": "explorer.exe",
        "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        "firefox": "C:/Program Files/Mozilla Firefox/firefox.exe",
        "vs code": "code",
        "code": "code",
        "spotify": "spotify",
        "discord": "discord",
        "slack": "slack",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "outlook": "OUTLOOK.EXE",
        "terminal": "wt.exe",
        "settings": "ms-settings:",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "snipping tool": "SnippingTool.exe",
    }

    def __init__(self):
        self.logger = Logger().get_logger("APP_LAUNCHER")

    def launch(self, name: str, args: str = "") -> bool:
        """Launch an application by name."""
        cmd = self.COMMON_APPS.get(name.lower(), name)
        try:
            if args:
                cmd = f"{cmd} {args}"
            subprocess.Popen(cmd, shell=True)
            self.logger.info(f"Launched: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Launch failed: {name} - {e}")
            return False

    def launch_path(self, filepath: str) -> bool:
        """Open a file or folder with default application."""
        try:
            os.startfile(filepath)
            self.logger.info(f"Opened: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Open failed: {e}")
            return False

    def find_and_launch(self, name: str) -> bool:
        """Search PATH and launch an application."""
        try:
            result = subprocess.run(
                f"where {name}",
                shell=True, capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                path = result.stdout.strip().split("\n")[0]
                subprocess.Popen(path, shell=True)
                return True
        except:
            pass
        return self.launch(name)

    def list_running(self) -> List[Dict]:
        """List running processes (user-friendly)."""
        try:
            result = subprocess.run(
                "tasklist /FO CSV",
                shell=True, capture_output=True, text=True
            )
            lines = result.stdout.strip().split("\n")[1:]
            apps = []
            for line in lines[:30]:
                parts = line.strip('"').split('","')
                if len(parts) >= 2:
                    apps.append({"name": parts[0], "pid": parts[1]})
            return apps
        except:
            return []
