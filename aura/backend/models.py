from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from typing import Any


# ==================================================
# Document Metadata
# ==================================================

@dataclass(slots=True)
class DocumentMetadata:

    title: str = ""

    author: str = ""

    subject: str = ""

    pages: int = 0

    language: str = ""

    created: datetime = field(

        default_factory=datetime.now

    )

    metadata: dict[str, Any] = field(

        default_factory=dict

    )


# ==================================================
# Generation Options
# ==================================================

@dataclass(slots=True)
class GenerationOptions:

    model: str = "gemini-2.5-flash"

    temperature: float = 0.4

    max_tokens: int | None = None

    stream: bool = False

    extra: dict[str, Any] = field(

        default_factory=dict

    )


# ==================================================
# Generation Result
# ==================================================

@dataclass(slots=True)
class GenerationResult:

    generator: str

    title: str

    content: str

    success: bool = True

    created: datetime = field(

        default_factory=datetime.now

    )

    metadata: dict[str, Any] = field(

        default_factory=dict

    )


# ==================================================
# Study Project
# ==================================================

@dataclass(slots=True)
class StudyProject:

    name: str

    source: str

    created: datetime = field(

        default_factory=datetime.now

    )

    modified: datetime = field(

        default_factory=datetime.now

    )

    results: list[GenerationResult] = field(

        default_factory=list

    )

    metadata: dict[str, Any] = field(

        default_factory=dict

    )

    def add_result(

        self,

        result: GenerationResult

    ):

        self.results.append(

            result

        )

        self.modified = datetime.now()