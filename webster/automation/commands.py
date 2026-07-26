"""
WEBSTER Command Executor
===========================
Execute system commands safely and return output.
"""

import subprocess
import sys
import os
from typing import Optional, Dict
from webster.core.logger import Logger


class CommandExecutor:
    """Execute shell commands with safety checks."""

    SAFE_COMMANDS = [
        "dir", "ls", "cd", "pwd", "echo", "type", "cat", "find", "where",
        "python", "pip", "npm", "node", "git", "help", "ver", "systeminfo",
        "tasklist", "ipconfig", "ping", "tracert", "nslookup",
    ]

    def __init__(self):
        self.logger = Logger().get_logger("CMD_EXEC")
        self._last_output = ""

    def run(self, command: str, timeout: int = 30, shell: bool = True) -> Dict:
        """Run a command and return result."""
        self.logger.info(f"Executing: {command}")
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = result.stdout or result.stderr or ""
            self._last_output = output
            return {
                "success": result.returncode == 0,
                "output": output.strip(),
                "error": result.stderr.strip(),
                "return_code": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "output": "", "error": "Command timed out", "return_code": -1}
        except Exception as e:
            return {"success": False, "output": "", "error": str(e), "return_code": -1}

    def run_powershell(self, command: str, timeout: int = 30) -> Dict:
        """Run a PowerShell command."""
        return self.run(f"powershell -Command \"{command}\"", timeout=timeout)

    def run_python(self, code: str, timeout: int = 10) -> Dict:
        """Run a Python snippet."""
        return self.run(f'python -c "{code}"', timeout=timeout)

    def is_safe(self, command: str) -> bool:
        """Check if command is in safe list."""
        cmd = command.strip().split()[0].lower() if command.strip() else ""
        return cmd in self.SAFE_COMMANDS

    def last_output(self) -> str:
        return self._last_output
