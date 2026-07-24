"""Mind-map generator."""
from backend.ai.prompt_builder import PromptBuilder
from backend.generators.base_generator import BaseGenerator


class MindMapGenerator(BaseGenerator):

    def build_prompt(

        self,

        document,

        **kwargs

    ) -> str:

        self.validate(document)

        return PromptBuilder.mindmap(

            document.text

        )

    def process_response(

        self,

        response,

        document,

        **kwargs

    ):

        return self.create_result(

            document,

            response,

            output_type="mindmap"

        )