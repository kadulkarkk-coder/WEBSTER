"""
WEBSTER Sync Manager
=====================
Central sync coordinator that manages local + cloud sync.
"""

from typing import Any, Dict, Optional
from webster.core.logger import Logger
from webster.sync.local import LocalSync
from webster.sync.cloud import CloudSync


class SyncManager:
    """Coordinator for all synchronization operations."""

    def __init__(self):
        self.logger = Logger().get_logger("SYNC_MGR")
        self.local = LocalSync()
        self.cloud = CloudSync()
        self._auto_sync = True

    def backup_all(self, data: Dict) -> bool:
        for key, value in data.items():
            self.local.backup(key, value)
        if self.cloud.is_connected and self._auto_sync:
            for key, value in data.items():
                self.cloud.push(key, value)
        return True

    def restore_all(self, keys: list) -> Dict:
        result = {}
        for key in keys:
            data = self.local.restore(key)
            if data is not None:
                result[key] = data
        return result

    def enable_auto_sync(self):
        self._auto_sync = True

    def disable_auto_sync(self):
        self._auto_sync = False

    @property
    def is_auto_sync(self) -> bool:
        return self._auto_sync
