from aura.config.settings import Settings
from aura.utils.logger import Logger


class Launcher:

    def __init__(self):

        self.settings = Settings()

        self.logger = Logger()

    def start(self):
        self.logger.info("Starting AURA")

        print("=" * 40)
        print(f"{self.settings.get('app_name')} v{self.settings.get('version')}")
        print("=" * 40)

        print()

        print("Loading configuration...")

        print("✓ Configuration Loaded")

        print()

        print(f"Theme : {self.settings.get('theme')}")

        print()

        self.logger.info("AURA Started Successfully")

        print("Welcome to AURA!")