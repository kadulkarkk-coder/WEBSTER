from aura.config.branding import (
    APP_NAME,
    VERSION
)

class Launcher:
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def start(self):
        self.logger.info("Starting WEBSTER")

        print("=" * 40)
        print(f"{APP_NAME} v{VERSION}")
        print("=" * 40)

        print()

        print("Loading configuration...")

        print("✓ Configuration Loaded")

        print()

        print(f"Theme : {self.settings.get('theme')}")

        print()

        self.logger.info("WEBSTER Started Successfully")

        print("Welcome to WEBSTER!\nHi!\nI'm Spidey.\nHow can I help today?")