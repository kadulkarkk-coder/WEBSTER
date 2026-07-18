from aura.ai.providers.dummy_provider import DummyProvider
from aura.ai.providers.claude_provider import ClaudeProvider
from aura.ai.providers.gemini_provider import GeminiProvider


class ProviderFactory:
    """
    Creates AI providers.

    Sprint 21

        Dummy
        Gemini
        Ollama

    Future

        OpenAI
        Claude
        DeepSeek
    """

    _providers = {

        "dummy": DummyProvider,

        "gemini": GeminiProvider,

        "claude": ClaudeProvider

    }

    # ==================================================
    # Register
    # ==================================================

    @classmethod
    def register(

        cls,

        name,

        provider

    ):

        cls._providers[
            name.lower()
        ] = provider

    # ==================================================
    # Create
    # ==================================================

    @classmethod
    def create(

        cls,

        name

    ):

        provider = cls._providers.get(

            name.lower()

        )

        if provider is None:

            raise ValueError(

                f"Unknown provider '{name}'"

            )

        return provider()

    # ==================================================
    # Utilities
    # ==================================================

    @classmethod
    def exists(

        cls,

        name

    ):

        return name.lower() in cls._providers

    @classmethod
    def names(cls):

        return sorted(

            cls._providers.keys()

        )

    @classmethod
    def count(cls):

        return len(

            cls._providers

        )