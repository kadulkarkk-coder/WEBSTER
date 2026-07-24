"""
==================================================

                A.U.R.A.

            Glass Button Widget

Universal button used throughout AURA.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassButton(

    ctk.CTkButton

):

    """
    ==================================================

                Glass Button

    Universal button component.

    Example

        📤 Upload

        🤖 Generate

        ⚙️ Settings

    ==================================================
    """

    def __init__(

        self,

        master,

        text="",

        emoji="",

        command=None,

        width=160,

        height=42,

        corner_radius=12,

        state="normal",

        **kwargs

    ):

        self.theme = master.theme

        self.emoji = emoji

        self.label = (

            f"{emoji} {text}"

            if emoji

            else text

        )

        super().__init__(

            master,

            text=self.label,

            command=command,

            width=width,

            height=height,

            corner_radius=corner_radius,

            fg_color=self.theme.colors.primary,

            hover_color=self.theme.colors.hover,

            text_color=self.theme.colors.text,

            border_width=0,

            font=self.theme.fonts.body,

            state=state,

            **kwargs

        )

    # ==================================================
    # Text
    # ==================================================

    def set_text(

        self,

        text

    ):

        self.label = (

            f"{self.emoji} {text}"

            if self.emoji

            else text

        )

        self.configure(

            text=self.label

        )

    # ==================================================
    # Emoji
    # ==================================================

    def set_emoji(

        self,

        emoji

    ):

        self.emoji = emoji

        current = self.cget(

            "text"

        )

        if " " in current:

            current = current.split(

                " ",

                1

            )[1]

        self.configure(

            text=f"{emoji} {current}"

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            fg_color=self.theme.colors.primary,

            hover_color=self.theme.colors.hover,

            text_color=self.theme.colors.text

        )

    # ==================================================
    # States
    # ==================================================

    def enable(

        self

    ):

        self.configure(

            state="normal"

        )

    def disable(

        self

    ):

        self.configure(

            state="disabled"

        )

    # ==================================================
    # Loading
    # ==================================================

    def loading(

        self

    ):

        self.configure(

            state="disabled",

            text="⏳ Working..."

        )

    def ready(

        self,

        text=None

    ):

        self.configure(

            state="normal"

        )

        if text is not None:

            self.set_text(

                text

            )

    # ==================================================
    # Success
    # ==================================================

    def success(

        self,

        text="Done"

    ):

        self.configure(

            text=f"✅ {text}"

        )

    # ==================================================
    # Error
    # ==================================================

    def error(

        self,

        text="Failed"

    ):

        self.configure(

            text=f"❌ {text}"

        )

    # ==================================================
    # Warning
    # ==================================================

    def warning(

        self,

        text="Warning"

    ):

        self.configure(

            text=f"⚠️ {text}"

        )

    # ==================================================
    # Reset
    # ==================================================

    def reset(

        self,

        text

    ):

        self.set_text(

            text

        )

        self.enable()