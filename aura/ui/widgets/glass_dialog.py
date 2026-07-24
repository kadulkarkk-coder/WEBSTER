"""
==================================================

                A.U.R.A.

            Glass Dialog Widget

Universal dialog window.

Pure CustomTkinter
Emoji First

==================================================
"""

import customtkinter as ctk


class GlassDialog(

    ctk.CTkToplevel

):

    """
    ==================================================

                Glass Dialog

    Universal popup window.

    ==================================================
    """

    def __init__(

        self,

        master,

        title="Dialog",

        message="",

        emoji="ℹ️",

        width=420,

        height=220,

        modal=True,

        **kwargs

    ):

        self.theme = master.theme

        self.result = None

        super().__init__(

            master,

            fg_color=self.theme.colors.background,

            **kwargs

        )

        self.title(

            title

        )

        self.geometry(

            f"{width}x{height}"

        )

        self.resizable(

            False,

            False

        )

        if modal:

            self.transient(

                master

            )

            self.grab_set()

        self.grid_columnconfigure(

            0,

            weight=1

        )

        self.grid_rowconfigure(

            1,

            weight=1

        )

        self.header = ctk.CTkLabel(

            self,

            text=f"{emoji}  {title}",

            font=self.theme.fonts.title,

            text_color=self.theme.colors.text

        )

        self.header.grid(

            row=0,

            column=0,

            padx=25,

            pady=(

                20,

                10

            )

        )

        self.message = ctk.CTkLabel(

            self,

            text=message,

            justify="left",

            wraplength=340,

            font=self.theme.fonts.body,

            text_color=self.theme.colors.secondary_text

        )

        self.message.grid(

            row=1,

            column=0,

            padx=25,

            sticky="n"

        )

        self.button_frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.button_frame.grid(

            row=2,

            column=0,

            pady=(

                20,

                20

            )

        )

        self.cancel_button = ctk.CTkButton(

            self.button_frame,

            text="Cancel",

            width=110,

            command=self.cancel

        )

        self.cancel_button.pack(

            side="left",

            padx=8

        )

        self.ok_button = ctk.CTkButton(

            self.button_frame,

            text="OK",

            width=110,

            command=self.accept

        )

        self.ok_button.pack(

            side="left",

            padx=8

        )

        self.protocol(

            "WM_DELETE_WINDOW",

            self.cancel

        )

    # ==================================================
    # Actions
    # ==================================================

    def accept(

        self

    ):

        self.result = True

        self.destroy()

    def cancel(

        self

    ):

        self.result = False

        self.destroy()

    # ==================================================
    # Content
    # ==================================================

    def set_title(

        self,

        title,

        emoji="ℹ️"

    ):

        self.title(

            title

        )

        self.header.configure(

            text=f"{emoji}  {title}"

        )

    def set_message(

        self,

        message

    ):

        self.message.configure(

            text=message

        )

    # ==================================================
    # Button Text
    # ==================================================

    def set_ok_text(

        self,

        text

    ):

        self.ok_button.configure(

            text=text

        )

    def set_cancel_text(

        self,

        text

    ):

        self.cancel_button.configure(

            text=text

        )

    # ==================================================
    # Presets
    # ==================================================

    def success(

        self,

        message

    ):

        self.set_title(

            "Success",

            "✅"

        )

        self.set_message(

            message

        )

    def warning(

        self,

        message

    ):

        self.set_title(

            "Warning",

            "⚠️"

        )

        self.set_message(

            message

        )

    def error(

        self,

        message

    ):

        self.set_title(

            "Error",

            "❌"

        )

        self.set_message(

            message

        )

    def info(

        self,

        message

    ):

        self.set_title(

            "Information",

            "ℹ️"

        )

        self.set_message(

            message

        )

    # ==================================================
    # Wait
    # ==================================================

    def show(

        self

    ):

        self.wait_window()

        return self.result

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            fg_color=self.theme.colors.background

        )

        self.header.configure(

            text_color=self.theme.colors.text

        )

        self.message.configure(

            text_color=self.theme.colors.secondary_text

        )