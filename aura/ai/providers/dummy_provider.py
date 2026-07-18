import time

from aura.ai.providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):
    """
    ==================================================

                Dummy Provider

    ==================================================

    Used for testing the AI architecture.

    Behaves exactly like a real AI provider,
    except the responses are hard-coded.

    Sprint 21

        • Supports streaming
        • Supports provider switching
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        self.initialized = False

        self.version = "1.0"

    # ==================================================
    # Lifecycle
    # ==================================================

    def initialize(self):

        self.initialized = True

        print(
            "Dummy Provider Ready"
        )

    # --------------------------------------------------

    def shutdown(self):

        self.initialized = False

        print(
            "Dummy Provider Shutdown"
        )

    # ==================================================
    # AI
    # ==================================================

    def generate(

        self,

        prompt

    ):

        if not self.initialized:

            return "[ERROR] Dummy Provider is not initialized."

        return (

            "Hello!\n\n"

            "I am AURA's Dummy Provider.\n\n"

            "You said:\n\n"

            f"{prompt}"

        )

    # --------------------------------------------------

    def stream(

        self,

        prompt

    ):

        text = self.generate(

            prompt

        )


    # ==================================================
    # Information
    # ==================================================

    def get_name(self):

        return "Dummy"

    # --------------------------------------------------

    def get_status(self):

        if self.initialized:

            return "Online"

        return "Offline"

    # --------------------------------------------------

    def get_version(self):

        return self.version