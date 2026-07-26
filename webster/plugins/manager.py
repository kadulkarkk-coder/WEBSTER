"""
WEBSTER Plugin Manager
=======================
Load, enable, disable, and manage plugins dynamically.
"""

import os
import importlib
from typing import Any, Dict, List, Optional
from webster.core.logger import Logger
from webster.plugins.base import BasePlugin


class PluginManager:
    """Dynamic plugin loader and manager."""

    def __init__(self, plugin_dir: str = None):
        self.logger = Logger().get_logger("PLUGIN_MGR")
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_dir = plugin_dir or os.path.join("webster", "plugins")

    def register(self, plugin: BasePlugin):
        if plugin.name in self._plugins:
            self.logger.warning(f"Plugin '{plugin.name}' already registered")
            return
        self._plugins[plugin.name] = plugin
        plugin.on_load()
        self.logger.info(f"Plugin registered: {plugin.name} v{plugin.version}")

    def unregister(self, name: str):
        if name in self._plugins:
            self._plugins[name].on_unload()
            del self._plugins[name]

    def enable(self, name: str):
        if name in self._plugins:
            self._plugins[name].on_enable()

    def disable(self, name: str):
        if name in self._plugins:
            self._plugins[name].on_disable()

    def get(self, name: str) -> Optional[BasePlugin]:
        return self._plugins.get(name)

    def execute(self, name: str, action: str, **kwargs) -> Any:
        plugin = self.get(name)
        if plugin and plugin.is_enabled:
            return plugin.execute(action, **kwargs)
        return None

    def list_plugins(self) -> List[Dict]:
        return [p.get_manifest() for p in self._plugins.values()]

    def load_from_dir(self, directory: str = None):
        """Scan directory and load plugins."""
        directory = directory or self._plugin_dir
        if not os.path.isdir(directory):
            return
        for item in os.listdir(directory):
            if item.startswith("_") or item.startswith("."):
                continue
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                try:
                    module = importlib.import_module(f"webster.plugins.{item}")
                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                            self.register(obj())
                except Exception as e:
                    self.logger.error(f"Failed to load plugin '{item}': {e}")

    def count(self) -> int:
        return len(self._plugins)
