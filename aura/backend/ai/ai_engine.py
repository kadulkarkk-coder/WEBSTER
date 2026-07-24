"""AI engine integration module."""
from backend.ai.ai_request import AIRequest
from backend.ai.ai_response import AIResponse


class AIEngine:
    """
    ==================================================
                    AI Engine
    ==================================================

    Central entry point for every AI request.

    UI -> Generator -> AIEngine -> Provider

    ==================================================
    """

    def __init__(

        self,

        provider

    ):

        self.provider = provider

    def generate(

        self,

        request: AIRequest

    ) -> AIResponse:

        try:

            response = self.provider.generate(

                request

            )

            return response

        except Exception as error:

            return AIResponse(

                success=False,

                error=str(error)

            )

    def set_provider(

        self,

        provider

    ):

        self.provider = provider

    def provider_name(

        self

    ) -> str:

        return self.provider.__class__.__name__