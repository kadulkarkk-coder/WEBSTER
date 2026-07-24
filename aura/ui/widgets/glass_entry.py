"""
==================================================

                A.U.R.A.

             Glass Entry Widget

Universal text entry used throughout AURA.

Pure CustomTkinter
Emoji Ready

==================================================
"""

import customtkinter as ctk


class GlassEntry(

    ctk.CTkEntry

):

    """
    ==================================================

                Glass Entry

    Universal input field.

    Examples

        🔍 Search...

        💬 Ask AURA...

        📚 Chapter Name

    ==================================================
    """

    def __init__(

        self,

        master,

        placeholder="",

        width=320,

        height=42,

        corner_radius=12,

        textvariable=None,

        password=False,

        state="normal",

        **kwargs

    ):

        self.theme = master.theme

        super().__init__(

            master,

            width=width,

            height=height,

            corner_radius=corner_radius,

            textvariable=textvariable,

            placeholder_text=placeholder,

            fg_color=self.theme.colors.surface,

            border_color=self.theme.colors.border,

            text_color=self.theme.colors.text,

            placeholder_text_color=self.theme.colors.secondary_text,

            font=self.theme.fonts.body,

            state=state,

            show="•" if password else "",

            **kwargs

        )

    # ==================================================
    # Value
    # ==================================================

    def value(

        self

    ):

        return self.get().strip()

    def set(

        self,

        text

    ):

        self.delete(

            0,

            "end"

        )

        self.insert(

            0,

            text

        )

    def clear(

        self

    ):

        self.delete(

            0,

            "end"

        )

    # ==================================================
    # Focus
    # ==================================================

    def focus_entry(

        self

    ):

        self.focus()

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

    def readonly(

        self

    ):

        self.configure(

            state="readonly"

        )

    # ==================================================
    # Password
    # ==================================================

    def show_password(

        self

    ):

        self.configure(

            show=""

        )

    def hide_password(

        self

    ):

        self.configure(

            show="•"

        )

    # ==================================================
    # Placeholder
    # ==================================================

    def set_placeholder(

        self,

        text

    ):

        self.configure(

            placeholder_text=text

        )

    # ==================================================
    # Events
    # ==================================================

    def on_enter(

        self,

        callback

    ):

        self.bind(

            "<Return>",

            callback

        )

    def on_change(

        self,

        callback

    ):

        self.bind(

            "<KeyRelease>",

            callback

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.configure(

            fg_color=self.theme.colors.surface,

            border_color=self.theme.colors.border,

            text_color=self.theme.colors.text,

            placeholder_text_color=self.theme.colors.secondary_text

        )