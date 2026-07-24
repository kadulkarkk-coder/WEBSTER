"""
==================================================

                A.U.R.A.

          Glass Separator Widget

Universal separator used throughout AURA.

Pure CustomTkinter

==================================================
"""

import customtkinter as ctk


class GlassSeparator(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Separator

    Horizontal / Vertical divider.

    ==================================================
    """

    def __init__(

        self,

        master,

        orientation="horizontal",

        thickness=1,

        length=None,

        **kwargs

    ):

        self.theme = master.theme

        self.orientation = orientation

        self.thickness = thickness

        self.length = length

        if orientation == "horizontal":

            width = length

            height = thickness

        else:

            width = thickness

            height = length

        super().__init__(

            master,

            width=width,

            height=height,

            fg_color=self.theme.colors.border,

            corner_radius=0,

            **kwargs

        )

        self.grid_propagate(

            False

        )

    # ==================================================
    # Orientation
    # ==================================================

    def horizontal(

        self

    ):

        self.orientation = "horizontal"

        self.configure(

            width=self.length,

            height=self.thickness

        )

    def vertical(

        self

    ):

        self.orientation = "vertical"

        self.configure(

            width=self.thickness,

            height=self.length

        )

    # ==================================================
    # Thickness
    # ==================================================

    def set_thickness(

        self,

        thickness

    ):

        self.thickness = thickness

        if self.orientation == "horizontal":

            self.configure(

                height=thickness

            )

        else:

            self.configure(

                width=thickness

            )

    # ==================================================
    # Length
    # ==================================================

    def set_length(

        self,

        length

    ):

        self.length = length

        if self.orientation == "horizontal":

            self.configure(

                width=length

            )

        else:

            self.configure(

                height=length

            )

    # ==================================================
    # Color
    # ==================================================

    def set_color(

        self,

        color

    ):

        self.configure(

            fg_color=color

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            fg_color=self.theme.colors.border

        )

    # ==================================================
    # Helpers
    # ==================================================

    def hide(

        self

    ):

        self.grid_remove()

    def show(

        self

    ):

        self.grid()