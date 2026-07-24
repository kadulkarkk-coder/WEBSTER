from abc import ABC
from abc import abstractmethod

from backend.models import GenerationResult


class BaseGenerator(
    ABC
):
    """
    ==================================================

                    Base Generator

    ==================================================

    Base class for every AI generator.

    Flow

        Document
            │
            ▼
        Build Prompt
            │
            ▼
        AI Engine
            │
            ▼
        Process Response
            │
            ▼
        GenerationResult

    ==================================================
    """

    def __init__(

        self

    ):

        self.name = self.__class__.__name__

    # ==================================================
    # Build Prompt
    # ==================================================

    @abstractmethod
    def build_prompt(

        self,

        document,

        **kwargs

    ) -> str:

        """
        Build the prompt that will be sent to the AI.
        """

        raise NotImplementedError

    # ==================================================
    # Process Response
    # ==================================================

    @abstractmethod
    def process_response(

        self,

        response: str,

        document,

        **kwargs

    ) -> GenerationResult:

        """
        Convert the raw AI response into a
        GenerationResult object.
        """

        raise NotImplementedError

    # ==================================================
    # Validate Document
    # ==================================================

    def validate(

        self,

        document

    ):

        if document is None:

            raise ValueError(

                "Document cannot be None."

            )

        if not document.has_text():

            raise ValueError(

                "Document contains no text."

            )

    # ==================================================
    # Create Result
    # ==================================================

    def create_result(

        self,

        document,

        response: str,

        **metadata

    ) -> GenerationResult:

        return GenerationResult(

            generator=self.name,

            title=document.title,

            content=response,

            metadata=metadata

        )

    # ==================================================
    # Generator Metadata
    # ==================================================

    def metadata(

        self

    ) -> dict:

        return {

            "name": self.name,

            "version": "1.0",

            "supports_streaming": True

        }