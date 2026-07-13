class Plugin:
    """
    Base class for every AURA plugin.
    """

    def __init__(self):

        self.name = "Unknown Plugin"
        self.version = "1.0"

    def on_load(self):

        print(f"{self.name} loaded.")

    def on_unload(self):

        print(f"{self.name} unloaded.")