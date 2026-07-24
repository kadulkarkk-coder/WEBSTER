from typing import Any


class PreviewPipeline:
    """
    ==================================================

                    Preview Pipeline

    ==================================================

    Converts generated content into a format that
    can be displayed inside the Study Hub preview.

    Every generator sends its result here.

    ==================================================
    """

    def __init__(

        self

    ):

        self.current_data = None

        self.current_type = "text"

    # ==================================================
    # Update Preview
    # ==================================================

    def update(

        self,

        data: Any,

        preview_type: str = "text"

    ):

        self.current_data = data

        self.current_type = preview_type

    # ==================================================
    # Get Preview
    # ==================================================

    def get(

        self

    ) -> Any:

        return self.current_data

    # ==================================================
    # Type
    # ==================================================

    def preview_type(

        self

    ) -> str:

        return self.current_type

    # ==================================================
    # Clear
    # ==================================================

    def clear(

        self

    ):

        self.current_data = None

        self.current_type = "text"

    # ==================================================
    # Has Preview
    # ==================================================

    def has_preview(

        self

    ) -> bool:

        return self.current_data is not None

    # ==================================================
    # Markdown
    # ==================================================

    def markdown(

        self

    ) -> str:

        if self.current_data is None:

            return ""

        return str(

            self.current_data

        )

    # ==================================================
    # HTML
    # ==================================================

    def html(

        self

    ) -> str:

        if self.current_data is None:

            return ""

        text = str(

            self.current_data

        )

        return f"<pre>{text}</pre>"