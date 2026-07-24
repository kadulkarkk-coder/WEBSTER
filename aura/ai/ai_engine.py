from aura.ai.conversation_context import ConversationContext

from aura.ai.provider_manager import ProviderManager

class AIEngine:

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self

    ):

        self.provider_manager = ProviderManager()

        self.context = ConversationContext()
    # ==================================================
    # Provider
    # ==================================================

    def set_provider(

        self,

        provider

    ):

        provider.initialize()

        name = provider.get_name().lower()

        self.provider_manager.register(

            name,

            provider

        )

        self.provider_manager.activate(

            name

        )
    # ==================================================
    # Standard Response
    # ==================================================

    def ask(

        self,

        memory,

        prompt

    ):

        provider = self.provider_manager.current()

        if provider is None:

            return "No AI Provider Selected."

        final_prompt = self.context.build(

            memory,

            prompt

        )

        try:

            return provider.generate(

            final_prompt

            )

        except Exception:

            if self.provider_manager.failover():

                    provider = self.provider_manager.current()

                    return provider.generate(

                        final_prompt

                    )

            raise

    # ==================================================
    # Streaming Response
    # ==================================================

    def stream(

        self,

        memory,

        prompt

    ):

        provider = self.provider_manager.current()

        if provider is None:

            yield "No AI Provider Selected."

            return

        final_prompt = self.context.build(

            memory,

            prompt

        )

        if hasattr(

            provider,

            "stream"

        ):

            try:

                yield from provider.stream(

                    final_prompt

                )

            except Exception:

                if self.provider_manager.failover():

                    provider = self.provider_manager.current()

                    yield from provider.stream(

                            final_prompt

                    )

                else:

                    raise
                        
        else:

            yield provider.generate(

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

        return self.provider_manager.current()

    # --------------------------------------------------

    def get_provider_name(

        self

    ):

        provider = self.provider_manager.current()

        if provider:

            return provider.get_name()

        return "None"

    # --------------------------------------------------

    def get_provider_manager(

        self

    ):

        return self.provider_manager