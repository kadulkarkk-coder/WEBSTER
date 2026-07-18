class AIEngine:

    def __init__(self):

        self.provider = None

    # ==================================================
    # Provider
    # ==================================================

    def set_provider(
        self,
        provider
    ):

        self.provider = provider

        self.provider.initialize()

    # ==================================================
    # Standard Response
    # ==================================================

    def ask(
        self,
        context
    ):

        if self.provider is None:

            return "No AI Provider Selected."

        return self.provider.generate(
            context
        )

    # ==================================================
    # Streaming Response
    # ==================================================

    def stream(
        self,
        context
    ):

        if self.provider is None:

            yield "No AI Provider Selected."

            return

        if hasattr(
            self.provider,
            "stream"
        ):

            yield from self.provider.stream(
                context
            )

        else:

            yield self.provider.generate(
                context
            )
    # ==================================================
    # Info
    # ==================================================

    def get_provider(self):

        return self.provider

    def get_provider_name(self):

        if self.provider:

            return self.provider.get_name()

        return "None"