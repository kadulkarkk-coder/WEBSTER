"""Export pipeline."""
from backend.exporters.pdf_exporter import PDFExporter
from backend.exporters.docx_exporter import DOCXExporter
from backend.exporters.markdown_exporter import MarkdownExporter
from backend.exporters.ppt_exporter import PPTExporter
from backend.exporters.image_exporter import ImageExporter


class ExportPipeline:
    """
    ==================================================

                    Export Pipeline

    ==================================================

    Converts generated content into files.

    ==================================================
    """

    def __init__(

        self

    ):

        self.exporters = {

            "pdf": PDFExporter(),

            "docx": DOCXExporter(),

            "markdown": MarkdownExporter(),

            "pptx": PPTExporter(),

            "png": ImageExporter()

        }

    def export(

        self,

        data,

        output_path: str,

        export_type: str

    ):

        exporter = self.exporters.get(

            export_type.lower()

        )

        if exporter is None:

            raise ValueError(

                f"Unknown exporter: {export_type}"

            )

        exporter.export(

            data,

            output_path

        )