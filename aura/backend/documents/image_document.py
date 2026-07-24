"""Image document model."""
from dataclasses import dataclass

from backend.documents.document import Document


@dataclass(slots=True)
class ImageDocument(Document):
    """
    Image Document
    """

    width: int = 0

    height: int = 0

    ocr_text: str = ""

    def __init__(

        self,

        source: str

    ):

        super().__init__(

            source=source,

            document_type="image"

        )