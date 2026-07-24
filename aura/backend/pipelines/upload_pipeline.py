"""Upload pipeline."""
from pathlib import Path

from backend.documents.document import Document
from backend.parsers.pdf_parser import PDFParser
from backend.parsers.image_parser import ImageParser
from backend.parsers.text_parser import TextParser
from backend.parsers.website_parser import WebsiteParser


class UploadPipeline:
    """
    ==================================================

                    Upload Pipeline

    ==================================================

    Determines the correct parser for every source.

    ==================================================
    """

    def __init__(

        self

    ):

        self.parsers = {

            ".pdf": PDFParser(),

            ".png": ImageParser(),

            ".jpg": ImageParser(),

            ".jpeg": ImageParser(),

            ".bmp": ImageParser(),

            ".txt": TextParser(),

            ".md": TextParser()

        }

    def load(

        self,

        source: str

    ) -> Document:

        if source.startswith(

            "http://"

        ) or source.startswith(

            "https://"

        ):

            parser = WebsiteParser()

            return parser.parse(

                source

            )

        extension = Path(

            source

        ).suffix.lower()

        parser = self.parsers.get(

            extension

        )

        if parser is None:

            raise ValueError(

                f"Unsupported file type: {extension}"

            )

        return parser.parse(

            source

        )