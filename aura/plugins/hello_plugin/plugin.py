from aura.plugins.plugin import Plugin


class HelloPlugin(Plugin):

    def __init__(self):

        super().__init__()

        self.name = "Hello Plugin"

        self.version = "1.0"

    def on_load(self):

        print("Hello Plugin Loaded Successfully!")
