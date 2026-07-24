"""
==================================================

                A.U.R.A.

            Glass Panel Widget

High level container used for pages,
cards and major application sections.

Pure CustomTkinter
Emoji Ready

==================================================
"""

import customtkinter as ctk

from aura.ui.widgets.glass_frame import GlassFrame


class GlassPanel(

    GlassFrame

):

    """
    ==================================================

                    Glass Panel

    Reusable page container.

    Layout

        Emoji

        Title

        Subtitle

        ------------------

        Content

    ==================================================
    """

    def __init__(

        self,

        master,

        title="",

        emoji="",

        subtitle="",

        width=None,

        height=None,

        padding=20,

        **kwargs

    ):

        super().__init__(

            master,

            width=width,

            height=height,

            padding=padding,

            **kwargs

        )

        self.title = title

        self.subtitle = subtitle

        self.emoji = emoji

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

        self.grid_rowconfigure(

            1,

            weight=1

        )

        self.header = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.header.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=self.padding,

            pady=(

                self.padding,

                10

            )

        )

        self.header.grid_columnconfigure(

            1,

            weight=1

        )

        self.emoji_label = ctk.CTkLabel(

            self.header,

            text=self.emoji,

            font=self.fonts.emoji

        )

        self.emoji_label.grid(

            row=0,

            column=0,

            rowspan=2,

            padx=(

                0,

                12

            ),

            sticky="nw"

        )

        self.title_label = ctk.CTkLabel(

            self.header,

            text=self.title,

            font=self.fonts.title,

            anchor="w"

        )

        self.title_label.grid(

            row=0,

            column=1,

            sticky="w"

        )

        self.subtitle_label = ctk.CTkLabel(

            self.header,

            text=self.subtitle,

            font=self.fonts.small,

            anchor="w",

            text_color=self.colors.secondary_text

        )

        self.subtitle_label.grid(

            row=1,

            column=1,

            sticky="w"

        )

        self.separator = ctk.CTkFrame(

            self,

            height=1,

            fg_color=self.colors.border,

            corner_radius=0

        )

        self.separator.grid(

            row=1,

            column=0,

            sticky="ew",

            padx=self.padding,

            pady=(

                0,

                10

            )

        )

        self.content = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.content.grid(

            row=2,

            column=0,

            sticky="nsew",

            padx=self.padding,

            pady=(

                0,

                self.padding

            )

        )

        self.content.grid_rowconfigure(

            0,

            weight=1

        )

        self.content.grid_columnconfigure(

            0,

            weight=1

        )

    # ==================================================
    # Public
    # ==================================================

    def set_title(

        self,

        text

    ):

        self.title = text

        self.title_label.configure(

            text=text

        )

    def set_subtitle(

        self,

        text

    ):

        self.subtitle = text

        self.subtitle_label.configure(

            text=text

        )

    def set_emoji(

        self,

        emoji

    ):

        self.emoji = emoji

        self.emoji_label.configure(

            text=emoji

        )

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

    def hide_header(

        self

    ):

        self.header.grid_remove()

        self.separator.grid_remove()

    def show_header(

        self

    ):

        self.header.grid()

        self.separator.grid()

    def body(

        self

    ):

        return self.content

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        super().apply_theme()

        self.separator.configure(

            fg_color=self.colors.border

        )

        self.subtitle_label.configure(

            text_color=self.colors.secondary_text

        )

    # ==================================================
    # Helpers
    # ==================================================

    def clear_body(

        self

    ):

        for widget in self.content.winfo_children():

            widget.destroy()