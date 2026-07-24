"""PDF exporter."""
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph

from reportlab.lib.styles import getSampleStyleSheet

from backend.exporters.base_exporter import BaseExporter


class PDFExporter(
    BaseExporter
):

    def __init__(

        self

    ):

        super().__init__(

            ".pdf"

        )

    def export(

        self,

        result,

        output_path

    ):

        self.validate(

            output_path

        )

        styles = getSampleStyleSheet()

        document = SimpleDocTemplate(

            output_path

        )

        story = [

            Paragraph(

                result.content.replace(

                    "\n",

                    "<br/>"

                ),

                styles["BodyText"]

            )

        ]

        document.build(

            story

        )