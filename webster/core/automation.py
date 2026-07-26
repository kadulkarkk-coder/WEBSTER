"""
WEBSTER Automation Engine
==========================
Coordinates file management, app launching, browser control, and system operations.
"""

import os
import subprocess
import webbrowser
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

from webster.core.logger import Logger
from webster.core.errors import AutomationError


class AutomationEngine:
    """
    Handles system automation operations.
    File management, app launching, browser control, system commands.
    """

    def __init__(self):
        self.logger = Logger().get_logger("AUTOMATION")
        self._processes: Dict[str, subprocess.Popen] = {}
        self.logger.info("Automation engine initialized")

    def open_app(self, app_name: str) -> bool:
        """Open an application by name."""
        try:
            app_map = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe",
                "terminal": "cmd.exe",
                "explorer": "explorer.exe",
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
                "code": "code.exe",
                "vscode": "code.exe",
                "spotify": "spotify.exe",
                "word": "WINWORD.EXE",
                "excel": "EXCEL.EXE",
                "powerpoint": "POWERPNT.EXE",
            }
            target = app_map.get(app_name.lower(), app_name)
            subprocess.Popen([target], shell=True)
            self.logger.info(f"Opened app: {app_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open {app_name}: {e}")
            return False

    def close_app(self, app_name: str) -> bool:
        """Close an application by name."""
        try:
            subprocess.run(["taskkill", "/f", "/im", f"{app_name}.exe"], capture_output=True)
            self.logger.info(f"Closed app: {app_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to close {app_name}: {e}")
            return False

    def open_file(self, file_path: str) -> bool:
        """Open a file with default application."""
        try:
            os.startfile(file_path)
            self.logger.info(f"Opened file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open file: {e}")
            return False

    def open_folder(self, folder_path: str) -> bool:
        """Open a folder in Explorer."""
        try:
            subprocess.Popen(["explorer", folder_path])
            return True
        except Exception as e:
            self.logger.error(f"Failed to open folder: {e}")
            return False

    def open_url(self, url: str) -> bool:
        """Open a URL in the default browser."""
        try:
            webbrowser.open(url)
            self.logger.info(f"Opened URL: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open URL: {e}")
            return False

    def search_web(self, query: str) -> bool:
        """Search the web for a query."""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return self.open_url(url)

    def list_files(self, directory: str = ".") -> List[dict]:
        """List files in a directory."""
        files = []
        try:
            path = Path(directory)
            for item in path.iterdir():
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "size": item.stat().st_size if item.is_file() else 0,
                    "is_dir": item.is_dir(),
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                })
            files.sort(key=lambda f: (not f["is_dir"], f["name"]))
        except Exception as e:
            self.logger.error(f"Failed to list files: {e}")
        return files

    def create_file(self, file_path: str, content: str = "") -> bool:
        """Create a new file with optional content."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            self.logger.info(f"Created file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create file: {e}")
            return False

    def create_folder(self, folder_path: str) -> bool:
        """Create a new folder."""
        try:
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create folder: {e}")
            return False

    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            Path(file_path).unlink()
            self.logger.info(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file: {e}")
            return False

    def copy_file(self, source: str, dest: str) -> bool:
        """Copy a file to a new location."""
        try:
            shutil.copy2(source, dest)
            self.logger.info(f"Copied {source} to {dest}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to copy file: {e}")
            return False

    def move_file(self, source: str, dest: str) -> bool:
        """Move a file to a new location."""
        try:
            shutil.move(source, dest)
            self.logger.info(f"Moved {source} to {dest}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to move file: {e}")
            return False

    def read_file(self, file_path: str) -> Optional[str]:
        """Read file contents."""
        try:
            return Path(file_path).read_text(encoding="utf-8")
        except Exception as e:
            self.logger.error(f"Failed to read file: {e}")
            return None

    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to a file."""
        try:
            Path(file_path).write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            self.logger.error(f"Failed to write file: {e}")
            return False

    def get_system_info(self) -> dict:
        """Get basic system information."""
        import platform
        return {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": platform.python_version(),
        }

    def run_command(self, command: str) -> Tuple[str, str]:
        """Run a shell command and return output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return "", "Command timed out"
        except Exception as e:
            return "", str(e)

    def get_drives(self) -> List[str]:
        """Get available drives on Windows."""
        drives = []
        try:
            import string
            from ctypes import windll
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1
        except:
            pass
        return drives

    def status(self) -> dict:
        return {"active": True, "processes": len(self._processes)}
