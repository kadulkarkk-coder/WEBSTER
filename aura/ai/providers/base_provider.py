from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):
    """
    ==================================================

                Base AI Provider

    ==================================================

    Every AI provider must inherit from this class.

    Providers

        • Dummy
        • Gemini
        • Ollama
        • OpenAI
        • Claude
        • DeepSeek

    Required Methods

        initialize()
        shutdown()
        generate()
        stream()
        get_name()
        get_status()
        get_version()
    """

    # ==================================================
    # Lifecycle
    # ==================================================

    @abstractmethod
    def initialize(self):
        """
        Prepare the provider.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Cleanup before closing.
        """
        pass

    # ==================================================
    # AI
    # ==================================================

    @abstractmethod
    def generate(
        self,
        prompt
    ):
        """
        Standard response.
        """
        pass

    @abstractmethod
    def stream(
        self,
        prompt
    ):
        """
        Streaming response.
        """
        pass

    # ==================================================
    # Information
    # ==================================================

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def get_version(self):
        pass