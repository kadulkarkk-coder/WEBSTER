import json

from pathlib import Path


class APIKeys:

    def __init__(self):

        root = Path(__file__).resolve().parent.parent.parent

        self.path = root / "config" / "api_keys.json"

        self.data = {}

        self.load()

    # ==========================================

    def load(self):

        if not self.path.exists():

            self.data = {}

            return

        with open(

            self.path,

            "r",

            encoding="utf-8"

        ) as file:

            self.data = json.load(file)

    # ==========================================

    def save(self):

        with open(

            self.path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.data,

                file,

                indent=4

            )

    # ==========================================

    def get(self, provider):

        return self.data.get(

            provider,

            ""

        )

    # ==========================================

    def set(

        self,

        provider,

        key

    ):

        self.data[provider] = key

        self.save()