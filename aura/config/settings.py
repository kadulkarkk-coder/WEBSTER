import json
from pathlib import Path


class Settings:
    """
    Loads application settings from config/settings.json
    """

    def __init__(self):

        self.config_path = Path("config/settings.json")

        self.data = {}

        self.load()

    def load(self):

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found:\n{self.config_path}"
            )

        with open(self.config_path, "r", encoding="utf-8") as file:

            self.data = json.load(file)

    def get(self, key, default=None):

        return self.data.get(key, default)