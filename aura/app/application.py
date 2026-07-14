from aura.config.settings import Settings
from aura.utils.logger import Logger
from aura.core.launcher import Launcher
from aura.services.service_manager import ServiceManager
from aura.plugins.plugin_manager import PluginManager
from aura.plugins.hello_plugin.plugin import HelloPlugin
from aura.ui.main_window import MainWindow

class Application:

    def __init__(self):

        self.services = ServiceManager()

        settings = Settings()
        logger = Logger()

        self.services.register("settings", settings)
        self.services.register("logger", logger)

        launcher = Launcher(
            settings=settings,
            logger=logger
        )

        self.services.register("launcher", launcher)

        plugin_manager = PluginManager()

        self.services.register(
            "plugin_manager",
            plugin_manager
        )

        plugin = HelloPlugin()

        plugin_manager.register(plugin)

    def run(self):

        logger = self.services.get("logger")

        logger.info("Application Starting")

        launcher = self.services.get("launcher")

        launcher.start()

        window = MainWindow()
        window.mainloop()

        print("\nRegistered Services:")

        for service in self.services.list_services():
            print("-", service)

        print()

        plugin_manager = self.services.get("plugin_manager")

        print()
        print("Loaded Plugins:")

        for plugin in plugin_manager.list_plugins():
            print(f"- {plugin.name} ({plugin.version})")

        print()

        launcher.start()

        logger.info("Application Closed")