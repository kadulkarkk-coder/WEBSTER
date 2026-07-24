"""PDF document model."""
from dataclasses import dataclass

from backend.documents.document import Document


@dataclass(slots=True)
class PDFDocument(Document):
    """
    PDF Document
    """

    pages: int = 0

    encrypted: bool = False

    def __init__(

        self,

        source: str

    ):

        super().__init__(

            source=source,

            document_type="pdf"

        )