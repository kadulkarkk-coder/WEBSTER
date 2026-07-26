"""
WEBSTER File Manager
=====================
File operations: create, read, move, copy, delete, search files.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from webster.core.logger import Logger


class FileManager:
    """Manage files and directories on the system."""

    def __init__(self):
        self.logger = Logger().get_logger("FILE_MGR")

    def list_dir(self, path: str = ".") -> List[Dict]:
        """List contents of a directory."""
        try:
            items = []
            for item in os.scandir(path):
                info = {
                    "name": item.name,
                    "path": item.path,
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                }
                items.append(info)
            return sorted(items, key=lambda x: (-x["is_dir"], x["name"]))
        except Exception as e:
            self.logger.error(f"List dir error: {e}")
            return []

    def read_text(self, filepath: str) -> Optional[str]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Read error: {e}")
            return None

    def write_text(self, filepath: str, content: str) -> bool:
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Write error: {e}")
            return False

    def create_file(self, filepath: str, content: str = "") -> bool:
        return self.write_text(filepath, content)

    def create_dir(self, dirpath: str) -> bool:
        try:
            Path(dirpath).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Create dir error: {e}")
            return False

    def delete(self, path: str) -> bool:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return True
        except Exception as e:
            self.logger.error(f"Delete error: {e}")
            return False

    def copy(self, src: str, dst: str) -> bool:
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return True
        except Exception as e:
            self.logger.error(f"Copy error: {e}")
            return False

    def move(self, src: str, dst: str) -> bool:
        try:
            shutil.move(src, dst)
            return True
        except Exception as e:
            self.logger.error(f"Move error: {e}")
            return False

    def search(self, query: str, root: str = ".", max_results: int = 20) -> List[Dict]:
        """Search for files by name."""
        results = []
        for root_dir, _, files in os.walk(root):
            for file in files:
                if query.lower() in file.lower():
                    path = os.path.join(root_dir, file)
                    results.append({
                        "name": file,
                        "path": path,
                        "size": os.path.getsize(path),
                    })
                    if len(results) >= max_results:
                        return results
        return results

    def get_size(self, path: str) -> int:
        """Get file or directory size in bytes."""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            total = 0
            for dirpath, _, files in os.walk(path):
                for f in files:
                    fp = os.path.join(dirpath, f)
                    total += os.path.getsize(fp)
            return total
        except:
            return 0

    def get_info(self, path: str) -> Optional[Dict]:
        """Get detailed file information."""
        try:
            stat = os.stat(path)
            return {
                "name": os.path.basename(path),
                "path": os.path.abspath(path),
                "is_dir": os.path.isdir(path),
                "is_file": os.path.isfile(path),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            }
        except:
            return None
