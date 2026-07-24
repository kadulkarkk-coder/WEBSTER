import customtkinter as ctk

from aura.theme.loader import AssetLoader


class GlassIcon(ctk.CTkLabel):

    """
    ==================================================

                    Glass Icon

    Displays an text from assets.

    Uses:
        assets/themes/<theme>/icons/

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        category,

        name,

        size=(24, 24),

        **kwargs

    ):

        self.category = category

        self.name = name

        self.size = size

        self.text = AssetLoader.text(

            category,

            name,

            size

        )

        super().__init__(

            master,

            text="",

            image=self.text,

            fg_color="transparent",

            **kwargs

        )

    # ==================================================
    # Change Icon
    # ==================================================

    def set_icon(

        self,

        category,

        name,

        size=None

    ):

        if size is None:

            size = self.size

        self.category = category

        self.name = name

        self.size = size

        self.text = AssetLoader.text(

            category,

            name,

            size

        )

        self.configure(

            image=self.text

        )

    # ==================================================
    # Resize
    # ==================================================

    def resize(

        self,

        width,

        height

    ):

        self.size = (

            width,

            height

        )

        self.set_icon(

            self.category,

            self.name,

            self.size

        )

    # ==================================================
    # Get Current Icon
    # ==================================================

    def get_icon(

        self

    ):

        return (

            self.category,

            self.name

        )