"""
==================================================

                A.U.R.A.

             Glass Bar Widget

Reusable horizontal container for

• Toolbars
• Status Bars
• Action Bars
• Search Bars

Pure CustomTkinter
Emoji Ready

==================================================
"""

import customtkinter as ctk

from aura.ui.widgets.glass_frame import GlassFrame


class GlassBar(

    GlassFrame

):

    """
    ==================================================

                    Glass Bar

    Horizontal container for controls.

    ==================================================
    """

    def __init__(

        self,

        master,

        height=60,

        padding=12,

        spacing=10,

        **kwargs

    ):

        super().__init__(

            master,

            height=height,

            padding=padding,

            **kwargs

        )

        self.spacing = spacing

        self.widgets = []

        self._build()

    # ==================================================
    # Build
    # ==================================================

    def _build(

        self

    ):

        self.grid_rowconfigure(

            0,

            weight=1

        )

        self.grid_columnconfigure(

            999,

            weight=1

        )

    # ==================================================
    # Add
    # ==================================================

    def add(

        self,

        widget,

        expand=False,

        padx=None

    ):

        column = len(

            self.widgets

        )

        self.grid_columnconfigure(

            column,

            weight=1 if expand else 0

        )

        widget.grid(

            row=0,

            column=column,

            padx=(

                padx
                if padx is not None
                else self.spacing

            ),

            pady=self.padding,

            sticky="ew"

            if expand

            else "w"

        )

        self.widgets.append(

            widget

        )

        return widget

    # ==================================================
    # Spacer
    # ==================================================

    def add_spacer(

        self

    ):

        column = len(

            self.widgets

        )

        spacer = ctk.CTkFrame(

            self,

            fg_color="transparent",

            width=1

        )

        self.grid_columnconfigure(

            column,

            weight=1

        )

        spacer.grid(

            row=0,

            column=column,

            sticky="ew"

        )

        self.widgets.append(

            spacer

        )

    # ==================================================
    # Separator
    # ==================================================

    def add_separator(

        self,

        height=28

    ):

        separator = ctk.CTkFrame(

            self,

            width=1,

            height=height,

            fg_color=self.colors.border,

            corner_radius=0

        )

        self.add(

            separator

        )

    # ==================================================
    # Remove
    # ==================================================

    def remove(

        self,

        widget

    ):

        if widget in self.widgets:

            self.widgets.remove(

                widget

            )

            widget.destroy()

    # ==================================================
    # Clear
    # ==================================================

    def clear(

        self

    ):

        for widget in self.widgets:

            widget.destroy()

        self.widgets.clear()

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        super().apply_theme()

    # ==================================================
    # Helpers
    # ==================================================

    def count(

        self

    ):

        return len(

            self.widgets

        )

    def is_empty(

        self

    ):

        return (

            len(

                self.widgets

            )

            ==

            0

        )