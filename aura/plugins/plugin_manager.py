from aura.plugins.plugin import Plugin


class PluginManager:

    def __init__(self):

        self.plugins = []

    def register(self, plugin: Plugin):

        self.plugins.append(plugin)

        plugin.on_load()

    def unregister(self, plugin: Plugin):

        plugin.on_unload()

        self.plugins.remove(plugin)

    def list_plugins(self):

        return self.plugins

    def count(self):

        return len(self.plugins)