class AIEngine:

    def __init__(self):

        self.provider = None

    def set_provider(self, provider):

        self.provider = provider

        self.provider.initialize()

    def ask(self, prompt):

        if self.provider is None:

            return "No AI Provider Selected."

        return self.provider.generate(prompt)

    def get_provider(self):

        return self.provider

    def get_provider_name(self):

        if self.provider:

            return self.provider.get_name()

        return "None"