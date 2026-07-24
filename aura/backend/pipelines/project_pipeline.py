from pathlib import Path
import json


class ProjectPipeline:
    """
    ==================================================

                    Project Pipeline

    ==================================================

    Handles Study Hub project storage.

    Save

    Load

    Delete

    Autosave

    ==================================================
    """

    def __init__(

        self,

        workspace="projects"

    ):

        self.workspace = Path(

            workspace

        )

        self.workspace.mkdir(

            parents=True,

            exist_ok=True

        )

    # ==================================================
    # Save
    # ==================================================

    def save(

        self,

        name,

        data

    ):

        file = self.workspace / f"{name}.json"

        with open(

            file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )

        return file

    # ==================================================
    # Load
    # ==================================================

    def load(

        self,

        name

    ):

        file = self.workspace / f"{name}.json"

        if not file.exists():

            return None

        with open(

            file,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(

                f

            )

    # ==================================================
    # Exists
    # ==================================================

    def exists(

        self,

        name

    ):

        file = self.workspace / f"{name}.json"

        return file.exists()

    # ==================================================
    # Delete
    # ==================================================

    def delete(

        self,

        name

    ):

        file = self.workspace / f"{name}.json"

        if file.exists():

            file.unlink()

    # ==================================================
    # List
    # ==================================================

    def projects(

        self

    ):

        return sorted(

            [

                file.stem

                for file in self.workspace.glob(

                    "*.json"

                )

            ]

        )

    # ==================================================
    # Autosave
    # ==================================================

    def autosave(

        self,

        data

    ):

        self.save(

            "_autosave",

            data

        )

    # ==================================================
    # Load Autosave
    # ==================================================

    def load_autosave(

        self

    ):

        return self.load(

            "_autosave"

        )

    # ==================================================
    # Clear Autosave
    # ==================================================

    def clear_autosave(

        self

    ):

        self.delete(

            "_autosave"

        )