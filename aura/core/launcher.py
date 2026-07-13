from aura.config.settings import Settings
from aura.utils.logger import Logger


class Launcher:

    def __init__(self):

        self.settings = Settings()

        self.logger = Logger()

    def start(self):

        print("=" * 40)
        print(
            f"{self.settings.get('app_name')} v{self.settings.get('version')}"
        )
        print("=" * 40)

        print()

        print("Loading configuration...")

        print("✓ Configuration Loaded")

        print()

        print(f"App Name : {self.settings.get('app_name')}")
        print(f"Version  : {self.settings.get('version')}")
        print(f"Theme    : {self.settings.get('theme')}")

        print()

        print("Starting AURA...")

        self.logger.info("AURA Started Successfully")
        self.logger.info("Configuration Loaded")
        self.logger.debug("Debug Mode Enabled")
        self.logger.warning("This is only a test warning.")

        print()

        print("Welcome to AURA!")