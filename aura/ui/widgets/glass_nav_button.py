"""
==================================================

                A.U.R.A.

          Glass Navigation Button

Navigation button used in the Sidebar.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassNavButton(

    ctk.CTkButton

):

    """
    ==================================================

                Glass Navigation Button

    Sidebar navigation component.

    Example

        🏠 Dashboard

        💬 Chat

        📚 Study Hub

    ==================================================
    """

    def __init__(

        self,

        master,

        text="",

        emoji="",

        command=None,

        width=220,

        height=48,

        selected=False,

        **kwargs

    ):

        self.theme = master.theme

        self.emoji = emoji

        self.title = text

        self.selected = selected

        super().__init__(

            master,

            text=f"{emoji}  {text}",

            command=command,

            width=width,

            height=height,

            corner_radius=12,

            anchor="w",

            fg_color=self._background(),

            hover_color=self.theme.colors.hover,

            text_color=self._text_color(),

            font=self.theme.fonts.body,

            border_width=0,

            **kwargs

        )

    # ==================================================
    # Colors
    # ==================================================

    def _background(

        self

    ):

        if self.selected:

            return self.theme.colors.accent

        return "transparent"

    def _text_color(

        self

    ):

        if self.selected:

            return self.theme.colors.on_accent

        return self.theme.colors.text

    # ==================================================
    # Selection
    # ==================================================

    def select(

        self

    ):

        self.selected = True

        self.configure(

            fg_color=self.theme.colors.accent,

            text_color=self.theme.colors.on_accent

        )

    def deselect(

        self

    ):

        self.selected = False

        self.configure(

            fg_color="transparent",

            text_color=self.theme.colors.text

        )

    def toggle(

        self

    ):

        if self.selected:

            self.deselect()

        else:

            self.select()

    # ==================================================
    # Text
    # ==================================================

    def set_text(

        self,

        text

    ):

        self.title = text

        self.configure(

            text=f"{self.emoji}  {text}"

        )

    # ==================================================
    # Emoji
    # ==================================================

    def set_emoji(

        self,

        emoji

    ):

        self.emoji = emoji

        self.configure(

            text=f"{emoji}  {self.title}"

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            fg_color=self._background(),

            hover_color=self.theme.colors.hover,

            text_color=self._text_color()

        )

    # ==================================================
    # Enable
    # ==================================================

    def enable(

        self

    ):

        self.configure(

            state="normal"

        )

    # ==================================================
    # Disable
    # ==================================================

    def disable(

        self

    ):

        self.configure(

            state="disabled"

        )

    # ==================================================
    # Helpers
    # ==================================================

    def is_selected(

        self

    ):

        return self.selected