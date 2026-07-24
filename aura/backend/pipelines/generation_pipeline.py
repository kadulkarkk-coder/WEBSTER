"""Generation pipeline."""
from backend.ai.ai_engine import AIEngine
from backend.ai.ai_request import AIRequest
from backend.ai.prompt_builder import PromptBuilder


class GenerationPipeline:
    """
    ==================================================

                Generation Pipeline

    ==================================================

    Central AI workflow.

    Document

        ↓

    Prompt

        ↓

    AI

        ↓

    Result

    ==================================================
    """

    def __init__(

        self,

        ai_engine: AIEngine

    ):

        self.ai = ai_engine

    def generate(

        self,

        document,

        generator,

        **kwargs

    ):

        prompt = generator.build_prompt(

            document,

            **kwargs

        )

        request = AIRequest(

            prompt=prompt,

            temperature=kwargs.get(

                "temperature",

                0.4

            ),

            model=kwargs.get(

                "model",

                "gemini-2.5-flash"

            )

        )

        response = self.ai.generate(

            request

        )

        if not response.success:

            raise RuntimeError(

                response.error

            )

        return generator.process_response(

            response.text,

            document,

            **kwargs

        )