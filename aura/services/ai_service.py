from aura.ai.ai_engine import AIEngine

from aura.ai.providers.dummy_provider import DummyProvider


class AIService:

    def __init__(self):

        self.engine = AIEngine()

    def initialize(self):

        self.engine.set_provider(
            DummyProvider()
        )

        print("AI Service Initialized")

    def ask(self, prompt):

        return self.engine.ask(prompt)

    def get_provider(self):

        return self.engine.get_provider_name()

    def get_status(self):

        return "Online"