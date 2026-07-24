"""Prompt construction utilities."""
class PromptBuilder:
    """
    ==================================================
                Prompt Builder
    ==================================================

    Centralized prompt creation.

    Every AI feature should build prompts here instead
    of embedding prompt strings throughout the codebase.

    ==================================================
    """

    @staticmethod
    def build(

        instruction: str,

        content: str,

        context: str = ""

    ) -> str:

        prompt = f"""
SYSTEM CONTEXT
--------------
{context}

TASK
----
{instruction}

CONTENT
-------
{content}

IMPORTANT
---------
Produce a clear, structured, high-quality answer.
"""

        return prompt.strip()

    @staticmethod
    def notes(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction=(
                "Create detailed study notes using headings, "
                "bullet points, definitions, examples, "
                "and revision tips."
            ),

            content=content

        )

    @staticmethod
    def summary(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Create a concise chapter summary.",

            content=content

        )

    @staticmethod
    def quiz(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Generate quiz questions from the content.",

            content=content

        )

    @staticmethod
    def flashcards(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Generate flashcards from the content.",

            content=content

        )

    @staticmethod
    def worksheet(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Generate a worksheet for students.",

            content=content

        )

    @staticmethod
    def speech(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Write an engaging speech.",

            content=content

        )

    @staticmethod
    def ppt(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Create presentation slides.",

            content=content

        )

    @staticmethod
    def mindmap(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Generate a hierarchical mind map.",

            content=content

        )

    @staticmethod
    def question_paper(

        content: str

    ) -> str:

        return PromptBuilder.build(

            instruction="Generate a complete question paper.",

            content=content

        )