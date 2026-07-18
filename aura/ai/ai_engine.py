from aura.ai.conversation_context import ConversationContext


class AIEngine:

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self

    ):

        self.provider = "gemini"

        self.context = ConversationContext()

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

        memory,

        prompt

    ):

        if self.provider is None:

            return "No AI Provider Selected."

        final_prompt = self.context.build(

            memory,

            prompt

        )

        return self.provider.generate(

            final_prompt

        )

    # ==================================================
    # Streaming Response
    # ==================================================

    def stream(

        self,

        memory,

        prompt

    ):

        if self.provider is None:

            yield "No AI Provider Selected."

            return

        final_prompt = self.context.build(

            memory,

            prompt

        )

        yield from self.provider.stream(

            final_prompt

        )

    # ==================================================
    # Context
    # ==================================================

    def get_context(

        self

    ):

        return self.context

    # ==================================================
    # Provider
    # ==================================================

    def get_provider(

        self

    ):

        return self.provider

    # --------------------------------------------------

    def get_provider_name(

        self

    ):

        if self.provider:

            return self.provider.get_name()

        return "None"