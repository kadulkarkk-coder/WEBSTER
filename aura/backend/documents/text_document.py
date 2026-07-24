"""Text document model."""
from dataclasses import dataclass

from backend.documents.document import Document


@dataclass(slots=True)
class TextDocument(Document):
    """
    Plain Text Document
    """

    encoding: str = "utf-8"

    line_count: int = 0

    def __init__(

        self,

        source: str

    ):

        super().__init__(

            source=source,

            document_type="text"

        )