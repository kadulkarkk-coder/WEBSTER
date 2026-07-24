from dataclasses import asdict
from pathlib import Path

import json

from backend.projects.project import Project


class ProjectSerializer:
    """
    ==================================================

                Project Serializer

    ==================================================
    """

    def save(

        self,

        project: Project,

        file: str

    ):

        path = Path(

            file

        )

        path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as fp:

            json.dump(

                asdict(

                    project

                ),

                fp,

                indent=4,

                ensure_ascii=False,

                default=str

            )

    def load(

        self,

        file: str

    ):

        path = Path(

            file

        )

        if not path.exists():

            return None

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as fp:

            return json.load(

                fp

            )