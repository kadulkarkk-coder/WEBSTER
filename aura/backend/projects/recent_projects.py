"""Recent-project tracking."""
from collections import deque


class RecentProjects:
    """
    ==================================================

                Recent Projects

    ==================================================
    """

    def __init__(

        self,

        maximum=10

    ):

        self.projects = deque(

            maxlen=maximum

        )

    # ==================================================
    # Add
    # ==================================================

    def add(

        self,

        project

    ):

        if project in self.projects:

            self.projects.remove(

                project

            )

        self.projects.appendleft(

            project

        )

    # ==================================================
    # List
    # ==================================================

    def list(

        self

    ):

        return list(

            self.projects

        )

    # ==================================================
    # Clear
    # ==================================================

    def clear(

        self

    ):

        self.projects.clear()