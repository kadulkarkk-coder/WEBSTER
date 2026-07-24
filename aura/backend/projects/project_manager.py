"""Project management service."""
from pathlib import Path

from backend.projects.project import Project
from backend.projects.project_serializer import ProjectSerializer


class ProjectManager:
    """
    ==================================================

                Project Manager

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

        self.serializer = ProjectSerializer()

        self.current = None

    # ==================================================
    # Create
    # ==================================================

    def create(

        self,

        name,

        source=""

    ):

        self.current = Project(

            name=name,

            source=source

        )

        return self.current

    # ==================================================
    # Current
    # ==================================================

    def current_project(

        self

    ):

        return self.current

    # ==================================================
    # Save
    # ==================================================

    def save(

        self

    ):

        if self.current is None:

            return

        file = self.workspace / (

            self.current.name + ".json"

        )

        self.serializer.save(

            self.current,

            str(file)

        )

    # ==================================================
    # Load
    # ==================================================

    def load(

        self,

        name

    ):

        file = self.workspace / (

            name + ".json"

        )

        return self.serializer.load(

            str(file)

        )

    # ==================================================
    # Delete
    # ==================================================

    def delete(

        self,

        name

    ):

        file = self.workspace / (

            name + ".json"

        )

        if file.exists():

            file.unlink()

    # ==================================================
    # List
    # ==================================================

    def list_projects(

        self

    ):

        return sorted(

            file.stem

            for file in self.workspace.glob(

                "*.json"

            )

        )