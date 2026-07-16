from aura.ai.providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):

    def initialize(self):
        print("Dummy Provider Ready")

    def generate(self, prompt: str) -> str:

        return (
            "Hello!\n\n"
            "I am AURA's Dummy Provider.\n\n"
            f"You said:\n{prompt}"
        )

    def get_name(self):
        return "Dummy"

    def get_status(self):
        return "Online"