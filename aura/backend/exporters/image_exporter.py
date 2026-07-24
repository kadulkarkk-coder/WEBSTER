"""Image exporter."""
from PIL import Image
from PIL import ImageDraw

from backend.exporters.base_exporter import BaseExporter


class ImageExporter(
    BaseExporter
):

    def __init__(

        self

    ):

        super().__init__(

            ".png"

        )

    def export(

        self,

        result,

        output_path

    ):

        self.validate(

            output_path

        )

        image = Image.new(

            "RGB",

            (1200, 1600),

            "white"

        )

        draw = ImageDraw.Draw(

            image

        )

        draw.multiline_text(

            (40, 40),

            result.content,

            fill="black"

        )

        image.save(

            output_path
        )