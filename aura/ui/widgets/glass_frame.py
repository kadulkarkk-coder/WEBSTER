"""
==================================================

                A.U.R.A.

            Glass Frame Widget

A reusable glass styled frame used throughout
the AURA interface.

Pure CustomTkinter
No Images
Emoji Ready

==================================================
"""

import customtkinter as ctk

from aura.theme.theme import Theme


class GlassFrame(

    ctk.CTkFrame

):

    """
    ==================================================

                    Glass Frame

    Base container for every major widget.

    ==================================================
    """

    def __init__(

        self,

        master,

        width=None,

        height=None,

        fg_color=None,

        border_color=None,

        border_width=1,

        corner_radius=18,

        padding=15,

        **kwargs

    ):

        self.theme = Theme

        super().__init__(

            master,

            width=width,

            height=height,

            fg_color=(
                fg_color
                or
                self.theme.colors.surface
            ),

            border_color=(
                border_color
                or
                self.theme.colors.border
            ),

            border_width=border_width,

            corner_radius=corner_radius,

            **kwargs

        )

        self.padding = padding

        self.grid_propagate(

            False

        )

    # ==================================================
    # Layout
    # ==================================================

    def apply_padding(

        self,

        widget,

        row,

        column=0,

        rowspan=1,

        columnspan=1,

        sticky="nsew"

    ):

        widget.grid(

            row=row,

            column=column,

            rowspan=rowspan,

            columnspan=columnspan,

            padx=self.padding,

            pady=self.padding,

            sticky=sticky

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            fg_color=self.theme.colors.surface,

            border_color=self.theme.colors.border

        )

    # ==================================================
    # Colors
    # ==================================================

    def set_color(

        self,

        color

    ):

        self.configure(

            fg_color=color

        )

    def set_border(

        self,

        color,

        width=1

    ):

        self.configure(

            border_color=color,

            border_width=width

        )

    # ==================================================
    # Radius
    # ==================================================

    def set_corner_radius(

        self,

        radius

    ):

        self.configure(

            corner_radius=radius

        )

    # ==================================================
    # Padding
    # ==================================================

    def set_padding(

        self,

        padding

    ):

        self.padding = padding

    # ==================================================
    # Enable
    # ==================================================

    def enable(

        self

    ):

        self.configure(

            border_width=1

        )

    # ==================================================
    # Disable
    # ==================================================

    def disable(

        self

    ):

        self.configure(

            border_width=0

        )

    # ==================================================
    # Refresh
    # ==================================================

    def refresh(

        self

    ):

        self.apply_theme()

        self.update_idletasks()

    # ==================================================
    # Clear
    # ==================================================

    def clear(

        self

    ):

        for child in self.winfo_children():

            child.destroy()

    # ==================================================
    # Helpers
    # ==================================================

    @property

    def colors(

        self

    ):

        return self.theme.colors

    @property

    def fonts(

        self

    ):

        return self.theme.fonts