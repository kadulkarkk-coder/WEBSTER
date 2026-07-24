"""
==================================================

                A.U.R.A.

            Glass Status Widget

Live status indicator.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassStatus(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Status

    Layout

        🟢 Ready

        Waiting for input...

    ==================================================
    """

    def __init__(

        self,

        master,

        status="Ready",

        message="Waiting for input...",

        emoji="🟢",

        **kwargs

    ):

        self.theme = master.theme

        self.status = status

        self.message = message

        self.emoji = emoji

        super().__init__(

            master,

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

            0,

            weight=1

        )

        self.status_label = ctk.CTkLabel(

            self,

            text=f"{self.emoji}  {self.status}",

            font=self.theme.fonts.subtitle,

            text_color=self.theme.colors.text,

            anchor="w"

        )

        self.status_label.grid(

            row=0,

            column=0,

            sticky="ew"

        )

        self.message_label = ctk.CTkLabel(

            self,

            text=self.message,

            font=self.theme.fonts.small,

            text_color=self.theme.colors.secondary_text,

            justify="left",

            anchor="w"

        )

        self.message_label.grid(

            row=1,

            column=0,

            sticky="ew",

            pady=(

                4,

                0

            )

        )

    # ==================================================
    # Status
    # ==================================================

    def set_status(

        self,

        emoji,

        status,

        message=""

    ):

        self.emoji = emoji

        self.status = status

        self.message = message

        self.status_label.configure(

            text=f"{emoji}  {status}"

        )

        self.message_label.configure(

            text=message

        )

    # ==================================================
    # Message
    # ==================================================

    def set_message(

        self,

        message

    ):

        self.message = message

        self.message_label.configure(

            text=message

        )

    # ==================================================
    # Ready
    # ==================================================

    def ready(

        self,

        message="Waiting for input..."

    ):

        self.set_status(

            "🟢",

            "Ready",

            message

        )

    # ==================================================
    # Working
    # ==================================================

    def working(

        self,

        message="Processing..."

    ):

        self.set_status(

            "⏳",

            "Working",

            message

        )

    # ==================================================
    # Success
    # ==================================================

    def success(

        self,

        message="Completed successfully."

    ):

        self.set_status(

            "✅",

            "Completed",

            message

        )

    # ==================================================
    # Warning
    # ==================================================

    def warning(

        self,

        message="Attention required."

    ):

        self.set_status(

            "⚠️",

            "Warning",

            message

        )

    # ==================================================
    # Error
    # ==================================================

    def error(

        self,

        message="Operation failed."

    ):

        self.set_status(

            "❌",

            "Error",

            message

        )

    # ==================================================
    # Offline
    # ==================================================

    def offline(

        self,

        message="Service unavailable."

    ):

        self.set_status(

            "🔴",

            "Offline",

            message

        )

    # ==================================================
    # AI
    # ==================================================

    def thinking(

        self,

        message="Generating response..."

    ):

        self.set_status(

            "🤖",

            "Thinking",

            message

        )

    # ==================================================
    # Voice
    # ==================================================

    def listening(

        self,

        message="Listening..."

    ):

        self.set_status(

            "🎤",

            "Listening",

            message

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.status_label.configure(

            text_color=self.theme.colors.text

        )

        self.message_label.configure(

            text_color=self.theme.colors.secondary_text

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

            "status":

                self.status,

            "message":

                self.message

        }