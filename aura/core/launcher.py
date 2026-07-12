from aura.config.settings import Settings
from aura.utils.logger import Logger


class Launcher:
    def __init__(self):
        self.settings = Settings()
        self.logger = Logger()

    def start(self):
        print("=" * 40)
        print("A.U.R.A. v0.0.1")
        print("=" * 40)

        self.logger.info("AURA Started")
        print("Welcome to AURA!")