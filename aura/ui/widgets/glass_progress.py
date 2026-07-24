"""
==================================================

                A.U.R.A.

           Glass Progress Widget

Universal progress indicator.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassProgress(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Progress

    Layout

        🤖 Processing...

        ████████████░░░░░░

        65%

    ==================================================
    """

    def __init__(

        self,

        master,

        text="Processing...",

        emoji="⏳",

        width=350,

        **kwargs

    ):

        self.theme = master.theme

        self.emoji = emoji

        self.text = text

        self.progress = 0.0

        super().__init__(

            master,

            fg_color="transparent",

            **kwargs

        )

        self._build(

            width

        )

    # ==================================================
    # Build
    # ==================================================

    def _build(

        self,

        width

    ):

        self.grid_columnconfigure(

            0,

            weight=1

        )

        self.header = ctk.CTkLabel(

            self,

            text=f"{self.emoji}  {self.text}",

            font=self.theme.fonts.body,

            anchor="w"

        )

        self.header.grid(

            row=0,

            column=0,

            sticky="ew",

            pady=(

                0,

                8

            )

        )

        self.bar = ctk.CTkProgressBar(

            self,

            width=width,

            height=14,

            corner_radius=8,

            fg_color=self.theme.colors.surface,

            border_color=self.theme.colors.border,

            border_width=1,

            progress_color=self.theme.colors.accent,

            mode="determinate"

        )

        self.bar.grid(

            row=1,

            column=0,

            sticky="ew"

        )

        self.bar.set(

            0

        )

        self.footer = ctk.CTkLabel(

            self,

            text="0%",

            font=self.theme.fonts.small,

            text_color=self.theme.colors.secondary_text,

            anchor="e"

        )

        self.footer.grid(

            row=2,

            column=0,

            sticky="e",

            pady=(

                6,

                0

            )

        )

    # ==================================================
    # Progress
    # ==================================================

    def set_progress(

        self,

        value

    ):

        value = max(

            0.0,

            min(

                1.0,

                value

            )

        )

        self.progress = value

        self.bar.set(

            value

        )

        self.footer.configure(

            text=f"{int(value * 100)}%"

        )

    # ==================================================
    # Status
    # ==================================================

    def set_text(

        self,

        text

    ):

        self.text = text

        self.header.configure(

            text=f"{self.emoji}  {text}"

        )

    def set_emoji(

        self,

        emoji

    ):

        self.emoji = emoji

        self.header.configure(

            text=f"{emoji}  {self.text}"

        )

    def set_status(

        self,

        emoji,

        text

    ):

        self.emoji = emoji

        self.text = text

        self.header.configure(

            text=f"{emoji}  {text}"

        )

    # ==================================================
    # Animation
    # ==================================================

    def start(

        self

    ):

        self.bar.configure(

            mode="indeterminate"

        )

        self.bar.start()

    def stop(

        self

    ):

        self.bar.stop()

        self.bar.configure(

            mode="determinate"

        )

    # ==================================================
    # States
    # ==================================================

    def success(

        self

    ):

        self.stop()

        self.set_status(

            "✅",

            "Completed"

        )

        self.set_progress(

            1.0

        )

    def error(

        self

    ):

        self.stop()

        self.set_status(

            "❌",

            "Failed"

        )

    def warning(

        self

    ):

        self.set_status(

            "⚠️",

            "Attention Required"

        )

    def reset(

        self

    ):

        self.stop()

        self.set_status(

            "⏳",

            "Processing..."

        )

        self.set_progress(

            0.0

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.bar.configure(

            fg_color=self.theme.colors.surface,

            border_color=self.theme.colors.border,

            progress_color=self.theme.colors.accent

        )

        self.header.configure(

            text_color=self.theme.colors.text

        )

        self.footer.configure(

            text_color=self.theme.colors.secondary_text

        )