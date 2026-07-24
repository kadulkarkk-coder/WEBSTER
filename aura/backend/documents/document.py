"""Base document model."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Document:
    """
    ==================================================
                    Base Document
    ==================================================

    Parent class for every document type.

    ==================================================
    """

    source: str

    document_type: str

    title: str = ""

    text: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def filename(

        self

    ) -> str:

        return Path(

            self.source

        ).name

    @property
    def extension(

        self

    ) -> str:

        return Path(

            self.source

        ).suffix.lower()

    def has_text(

        self

    ) -> bool:

        return bool(

            self.text.strip()

        )