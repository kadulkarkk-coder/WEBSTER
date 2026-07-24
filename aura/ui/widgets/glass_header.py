"""
==================================================

                A.U.R.A.

            Glass Header Widget

Universal page header.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassHeader(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Header

    Layout

        📚

        Study Hub

        Generate notes,
        quizzes and papers

    ==================================================
    """

    def __init__(

        self,

        master,

        emoji="",

        title="",

        subtitle="",

        height=90,

        **kwargs

    ):

        self.theme = master.theme

        self.emoji = emoji

        self.title = title

        self.subtitle = subtitle

        super().__init__(

            master,

            height=height,

            fg_color="transparent",

            **kwargs

        )

        self._build()

    # ==================================================
    # Build
    # ==================================================

    def _build(

        self

    ):

        self.grid_columnconfigure(

            1,

            weight=1

        )

        self.emoji_label = ctk.CTkLabel(

            self,

            text=self.emoji,

            font=self.theme.fonts.emoji

        )

        self.emoji_label.grid(

            row=0,

            column=0,

            rowspan=2,

            padx=(

                0,

                15

            ),

            sticky="nw"

        )

        self.title_label = ctk.CTkLabel(

            self,

            text=self.title,

            font=self.theme.fonts.title,

            anchor="w"

        )

        self.title_label.grid(

            row=0,

            column=1,

            sticky="sw"

        )

        self.subtitle_label = ctk.CTkLabel(

            self,

            text=self.subtitle,

            font=self.theme.fonts.small,

            text_color=self.theme.colors.secondary_text,

            anchor="w",

            justify="left"

        )

        self.subtitle_label.grid(

            row=1,

            column=1,

            sticky="nw"

        )

    # ==================================================
    # Header
    # ==================================================

    def set_header(

        self,

        emoji,

        title,

        subtitle=""

    ):

        self.set_emoji(

            emoji

        )

        self.set_title(

            title

        )

        self.set_subtitle(

            subtitle

        )

    # ==================================================
    # Emoji
    # ==================================================

    def set_emoji(

        self,

        emoji

    ):

        self.emoji = emoji

        self.emoji_label.configure(

            text=emoji

        )

    # ==================================================
    # Title
    # ==================================================

    def set_title(

        self,

        title

    ):

        self.title = title

        self.title_label.configure(

            text=title

        )

    # ==================================================
    # Subtitle
    # ==================================================

    def set_subtitle(

        self,

        subtitle

    ):

        self.subtitle = subtitle

        self.subtitle_label.configure(

            text=subtitle

        )

    # ==================================================
    # Visibility
    # ==================================================

    def hide_subtitle(

        self

    ):

        self.subtitle_label.grid_remove()

    def show_subtitle(

        self

    ):

        self.subtitle_label.grid()

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.title_label.configure(

            text_color=self.theme.colors.text

        )

        self.subtitle_label.configure(

            text_color=self.theme.colors.secondary_text

        )

    # ==================================================
    # Helpers
    # ==================================================

    def refresh(

        self

    ):

        self.apply_theme()

        self.update_idletasks()

    def data(

        self

    ):

        return {

            "emoji":

                self.emoji,

            "title":

                self.title,

            "subtitle":

                self.subtitle

        }