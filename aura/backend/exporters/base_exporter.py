from abc import ABC
from abc import abstractmethod

from pathlib import Path


class BaseExporter(
    ABC
):
    """
    ==================================================

                    Base Exporter

    ==================================================

    Parent exporter for every file format.

    ==================================================
    """

    def __init__(

        self,

        extension: str

    ):

        self.extension = extension

    # ==================================================
    # Export
    # ==================================================

    @abstractmethod
    def export(

        self,

        result,

        output_path: str

    ):

        raise NotImplementedError

    # ==================================================
    # Validate
    # ==================================================

    def validate(

        self,

        output_path: str

    ):

        folder = Path(

            output_path

        ).parent

        folder.mkdir(

            parents=True,

            exist_ok=True

        )