from aura.ai.ai_engine import AIEngine
from aura.ai.provider_factory import ProviderFactory

from aura.utils.debug import Debug


class AIService:
    """
    ==================================================

                    AI Service

    ==================================================

    Responsibilities

        • Manage AI Engine
        • Load Provider
        • Switch Provider
        • Generate Responses
        • Stream Responses
        • Report Status

    Sprint 21

        • Provider Factory
        • Runtime Provider Switching

    Future

        • Multiple Models
        • Provider Configuration
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        self.engine = AIEngine()

        self.provider_name = "dummy"

        self.initialized = False

    # ==================================================
    # Initialization
    # ==================================================

    def initialize(

        self,

        provider="dummy"

    ):

        Debug.log(

            "AI",

            f"Loading provider '{provider}'"

        )

        self.provider_name = provider.lower()

        provider_instance = ProviderFactory.create(

            self.provider_name

        )

        self.engine.set_provider(

            provider_instance

        )

        self.initialized = True

        Debug.log(

            "AI",

            f"Provider '{self.provider_name}' ready"

        )

    # ==================================================
    # Provider
    # ==================================================

    def change_provider(

        self,

        provider,

        memory=None

    ):

        provider = provider.lower()

        if provider == self.provider_name:

            return

        self.shutdown()

        self.initialize(

            provider

        )

        if memory:

            memory.set_setting(

               "provider",

               provider

           )

            memory.save()

        Debug.log(

           "AI",

           f"Provider changed to '{provider}'"

        )

    # ==================================================
    # AI
    # ==================================================

    def ask(

        self,

        prompt

    ):

        if not self.initialized:

            return "[ERROR] AI Service not initialized."

        if not prompt:

            return ""

        return self.engine.ask(

            prompt

        )

    # --------------------------------------------------

    def stream(

        self,

        prompt

    ):

        if not self.initialized:

            yield "[ERROR] AI Service not initialized."

            return

        if not prompt:

            return

        yield from self.engine.stream(

            prompt

        )

    # ==================================================
    # Status
    # ==================================================

    def is_ready(self):

        return self.initialized

    # --------------------------------------------------

    def get_status(self):

        if not self.initialized:

            return "Offline"

        provider = self.engine.get_provider()

        if provider:

            return provider.get_status()

        return "Offline"

    # --------------------------------------------------

    def get_provider_name(self):

        provider = self.engine.get_provider()

        if provider:

            return provider.get_name()

        return "None"

    # --------------------------------------------------

    def get_provider_version(self):

        provider = self.engine.get_provider()

        if provider:

            return provider.get_version()

        return "Unknown"

    # ==================================================
    # Shutdown
    # ==================================================

    def shutdown(self):

        provider = self.engine.get_provider()

        if provider:

            provider.shutdown()

        self.initialized = False

        Debug.log(

            "AI",

            "Provider shutdown"

        )