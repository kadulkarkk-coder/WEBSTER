import json
from pathlib import Path

from aura.exceptions.aura_exceptions import ConfigurationError


class Settings:

    def __init__(self):

        self.config_path = Path("config/settings.json")

        self.data = {}

        self.load()

    def load(self):

        if not self.config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found:\n{self.config_path}"
            )

        try:

            with open(self.config_path, "r", encoding="utf-8") as file:

                self.data = json.load(file)

        except json.JSONDecodeError as e:

            raise ConfigurationError(
                f"Invalid JSON configuration:\n{e}"
            )

    def get(self, key, default=None):

        return self.data.get(key, default)