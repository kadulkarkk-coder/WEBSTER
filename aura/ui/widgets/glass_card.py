"""
==================================================

                A.U.R.A.

             Glass Card Widget

Universal card component.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassCard(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Card

    Universal information card.

    Layout

        📄

        Title

        Subtitle

        Description

    ==================================================
    """

    def __init__(

        self,

        master,

        title="",

        subtitle="",

        description="",

        emoji="📄",

        width=320,

        height=180,

        command=None,

        **kwargs

    ):

        self.theme = master.theme

        self.command = command

        self.title = title

        self.subtitle = subtitle

        self.description = description

        self.emoji = emoji

        super().__init__(

            master,

            width=width,

            height=height,

            fg_color=self.theme.colors.surface,

            border_color=self.theme.colors.border,

            border_width=1,

            corner_radius=18,

            **kwargs

        )

        self.grid_propagate(

            False

        )

        self._build()

    # ==================================================
    # Build
    # ==================================================

    def _build(

        self

    ):

        self.grid_columnconfigure(

            0,

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

            pady=(

                20,

                10

            )

        )

        self.title_label = ctk.CTkLabel(

            self,

            text=self.title,

            font=self.theme.fonts.subtitle,

            text_color=self.theme.colors.text

        )

        self.title_label.grid(

            row=1,

            column=0,

            padx=20,

            sticky="w"

        )

        self.subtitle_label = ctk.CTkLabel(

            self,

            text=self.subtitle,

            font=self.theme.fonts.small,

            text_color=self.theme.colors.secondary_text

        )

        self.subtitle_label.grid(

            row=2,

            column=0,

            padx=20,

            sticky="w"

        )

        self.description_label = ctk.CTkLabel(

            self,

            text=self.description,

            justify="left",

            wraplength=280,

            anchor="nw",

            font=self.theme.fonts.body,

            text_color=self.theme.colors.text

        )

        self.description_label.grid(

            row=3,

            column=0,

            padx=20,

            pady=(

                10,

                20

            ),

            sticky="nsew"

        )

        self.bind(

            "<Button-1>",

            self._clicked

        )

        for widget in self.winfo_children():

            widget.bind(

                "<Button-1>",

                self._clicked

            )

    # ==================================================
    # Events
    # ==================================================

    def _clicked(

        self,

        event=None

    ):

        if self.command is not None:

            self.command()

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
    # Description
    # ==================================================

    def set_description(

        self,

        description

    ):

        self.description = description

        self.description_label.configure(

            text=description

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
    # Card
    # ==================================================

    def set_card(

        self,

        emoji,

        title,

        subtitle="",

        description=""

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

        self.set_description(

            description

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

        self.title_label.configure(

            text_color=self.theme.colors.text

        )

        self.subtitle_label.configure(

            text_color=self.theme.colors.secondary_text

        )

        self.description_label.configure(

            text_color=self.theme.colors.text

        )

    # ==================================================
    # Helpers
    # ==================================================

    def data(

        self

    ):

        return {

            "emoji":

                self.emoji,

            "title":

                self.title,

            "subtitle":

                self.subtitle,

            "description":

                self.description

        }