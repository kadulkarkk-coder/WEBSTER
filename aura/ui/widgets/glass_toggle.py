"""
==================================================

                A.U.R.A.

            Glass Toggle Widget

Universal switch used throughout AURA.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassToggle(

    ctk.CTkSwitch

):

    """
    ==================================================

                Glass Toggle

    Universal ON/OFF switch.

    Example

        🌙 Dark Mode

        🎤 Voice Input

        ☁️ Auto Sync

    ==================================================
    """

    def __init__(

        self,

        master,

        text="",

        emoji="",

        variable=None,

        command=None,

        width=180,

        height=32,

        state="normal",

        **kwargs

    ):

        self.theme = master.theme

        self.emoji = emoji

        self.title = text

        self.variable = (

            variable

            or

            ctk.BooleanVar(

                value=False

            )

        )

        super().__init__(

            master,

            text=f"{emoji}  {text}",

            variable=self.variable,

            command=command,

            width=width,

            height=height,

            switch_width=42,

            switch_height=22,

            corner_radius=100,

            fg_color=self.theme.colors.border,

            progress_color=self.theme.colors.accent,

            button_color=self.theme.colors.surface,

            button_hover_color=self.theme.colors.hover,

            text_color=self.theme.colors.text,

            font=self.theme.fonts.body,

            state=state,

            **kwargs

        )

    # ==================================================
    # State
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
    # Value
    # ==================================================

    def value(

        self

    ):

        return self.variable.get()

    def set(

        self,

        value

    ):

        self.variable.set(

            bool(

                value

            )

        )

    def on(

        self

    ):

        self.select()

    def off(

        self

    ):

        self.deselect()

    def toggle(

        self

    ):

        if self.value():

            self.off()

        else:

            self.on()

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

            fg_color=self.theme.colors.border,

            progress_color=self.theme.colors.accent,

            button_color=self.theme.colors.surface,

            button_hover_color=self.theme.colors.hover,

            text_color=self.theme.colors.text

        )

    # ==================================================
    # Helpers
    # ==================================================

    def is_on(

        self

    ):

        return self.value()

    def is_off(

        self

    ):

        return not self.value()