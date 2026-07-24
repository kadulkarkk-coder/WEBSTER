"""
==================================================

                A.U.R.A.

             Glass Badge Widget

Small badge used throughout AURA.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassBadge(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Badge

    Small information chip.

    Examples

        🟢 Online

        🤖 Gemini

        📄 PDF

    ==================================================
    """

    def __init__(

        self,

        master,

        text="",

        emoji="",

        fg_color=None,

        text_color=None,

        corner_radius=14,

        padx=10,

        pady=5,

        **kwargs

    ):

        self.theme = master.theme

        self.text = text

        self.emoji = emoji

        super().__init__(

            master,

            fg_color=(
                fg_color
                or
                self.theme.colors.surface
            ),

            border_color=self.theme.colors.border,

            border_width=1,

            corner_radius=corner_radius,

            **kwargs

        )

        self.label = ctk.CTkLabel(

            self,

            text=f"{emoji}  {text}",

            font=self.theme.fonts.small,

            text_color=(
                text_color
                or
                self.theme.colors.text
            )

        )

        self.label.pack(

            padx=padx,

            pady=pady

        )

    # ==================================================
    # Text
    # ==================================================

    def set_text(

        self,

        text

    ):

        self.text = text

        self.label.configure(

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

        self.label.configure(

            text=f"{emoji}  {self.text}"

        )

    # ==================================================
    # Badge
    # ==================================================

    def set_badge(

        self,

        emoji,

        text

    ):

        self.emoji = emoji

        self.text = text

        self.label.configure(

            text=f"{emoji}  {text}"

        )

    # ==================================================
    # Colors
    # ==================================================

    def set_colors(

        self,

        fg_color,

        text_color=None

    ):

        self.configure(

            fg_color=fg_color

        )

        if text_color is not None:

            self.label.configure(

                text_color=text_color

            )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            border_color=self.theme.colors.border

        )

        self.label.configure(

            text_color=self.theme.colors.text

        )

    # ==================================================
    # States
    # ==================================================

    def success(

        self,

        text="Ready"

    ):

        self.set_badge(

            "✅",

            text

        )

    def warning(

        self,

        text="Warning"

    ):

        self.set_badge(

            "⚠️",

            text

        )

    def error(

        self,

        text="Error"

    ):

        self.set_badge(

            "❌",

            text

        )

    def info(

        self,

        text="Info"

    ):

        self.set_badge(

            "ℹ️",

            text

        )