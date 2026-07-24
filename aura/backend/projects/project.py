"""Project model."""
from dataclasses import dataclass
from dataclasses import field

from datetime import datetime

from backend.models import GenerationResult


@dataclass(slots=True)
class Project:
    """
    ==================================================

                    Study Project

    ==================================================
    """

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

    metadata: dict = field(

        default_factory=dict

    )

    # ==================================================
    # Result
    # ==================================================

    def add_result(

        self,

        result: GenerationResult

    ):

        self.results.append(

            result

        )

        self.modified = datetime.now()

    # ==================================================
    # Clear
    # ==================================================

    def clear(

        self

    ):

        self.results.clear()

        self.modified = datetime.now()