"""
WEBSTER Local Sync
===================
Sync data to local storage (SQLite, JSON files).
"""

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from webster.core.logger import Logger


class LocalSync:
    """Synchronize data to local files for backup/restore."""

    def __init__(self, backup_dir: str = None):
        self.logger = Logger().get_logger("LOCAL_SYNC")
        self.backup_dir = backup_dir or os.path.join("webster", "data")

    def backup(self, name: str, data: Any) -> bool:
        """Backup data to a local file."""
        try:
            path = Path(self.backup_dir) / "backups" / f"{name}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Backup saved: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return False

    def restore(self, name: str) -> Optional[Any]:
        """Restore data from a local backup file."""
        try:
            path = Path(self.backup_dir) / "backups" / f"{name}.json"
            if not path.exists():
                return None
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            return None

    def list_backups(self) -> List[str]:
        backup_path = Path(self.backup_dir) / "backups"
        if not backup_path.exists():
            return []
        return [f.stem for f in backup_path.glob("*.json")]

    def delete_backup(self, name: str) -> bool:
        try:
            path = Path(self.backup_dir) / "backups" / f"{name}.json"
            if path.exists():
                path.unlink()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Delete backup failed: {e}")
            return False
