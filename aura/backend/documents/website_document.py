"""Website document model."""
from dataclasses import dataclass

from backend.documents.document import Document


@dataclass(slots=True)
class WebsiteDocument(Document):
    """
    Website Document
    """

    url: str = ""

    html: str = ""

    domain: str = ""

    def __init__(

        self,

        url: str

    ):

        super().__init__(

            source=url,

            document_type="website"

        )

        self.url = url