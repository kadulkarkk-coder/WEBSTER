"""Markdown exporter."""
from backend.exporters.base_exporter import BaseExporter


class MarkdownExporter(
    BaseExporter
):

    def __init__(

        self

    ):

        super().__init__(

            ".md"

        )

    def export(

        self,

        result,

        output_path

    ):

        self.validate(

            output_path

        )

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as file:

            file.write(

                result.content

            )