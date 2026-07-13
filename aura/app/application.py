from aura.config.settings import Settings
from aura.utils.logger import Logger
from aura.core.launcher import Launcher
from aura.services.service_manager import ServiceManager


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

    def run(self):

        logger = self.services.get("logger")

        logger.info("Application Starting")

        launcher = self.services.get("launcher")

        print("\nRegistered Services:")

        for service in self.services.list_services():
            print("-", service)

        print()

        launcher.start()

        logger.info("Application Closed")