"""
==================================================

                A.U.R.A.

            Glass Avatar Widget

Universal avatar component.

Pure CustomTkinter
Emoji + Image Support

==================================================
"""

import customtkinter as ctk


class GlassAvatar(

    ctk.CTkFrame

):

    """
    ==================================================

                Glass Avatar

    Examples

        🤖 AURA

        👤 User

        🧠 HELVAC

    ==================================================
    """

    def __init__(

        self,

        master,

        image=None,

        emoji="👤",

        name="",

        size=64,

        status="online",

        **kwargs

    ):

        self.theme = master.theme

        self.image = image

        self.emoji = emoji

        self.name = name

        self.size = size

        self.status = status

        super().__init__(

            master,

            width=size,

            height=size + 22,

            fg_color="transparent",

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

        self.avatar = ctk.CTkLabel(

            self,

            text=""

            if self.image

            else self.emoji,

            image=self.image,

            width=self.size,

            height=self.size,

            corner_radius=self.size // 2,

            fg_color=self.theme.colors.surface,

            text_color=self.theme.colors.text,

            font=self.theme.fonts.emoji

        )

        self.avatar.grid(

            row=0,

            column=0,

            padx=2,

            pady=(

                2,

                0

            )

        )

        self.indicator = ctk.CTkLabel(

            self,

            text=self._status_emoji(),

            font=self.theme.fonts.small

        )

        self.indicator.place(

            relx=1.0,

            rely=1.0,

            anchor="se"

        )

        self.name_label = ctk.CTkLabel(

            self,

            text=self.name,

            font=self.theme.fonts.small,

            text_color=self.theme.colors.secondary_text

        )

        self.name_label.grid(

            row=1,

            column=0,

            pady=(

                4,

                0

            )

        )

    # ==================================================
    # Status
    # ==================================================

    def _status_emoji(

        self

    ):

        return {

            "online": "🟢",

            "busy": "🟡",

            "offline": "🔴",

            "away": "⚪"

        }.get(

            self.status,

            "⚪"

        )

    def set_status(

        self,

        status

    ):

        self.status = status

        self.indicator.configure(

            text=self._status_emoji()

        )

    # ==================================================
    # Name
    # ==================================================

    def set_name(

        self,

        name

    ):

        self.name = name

        self.name_label.configure(

            text=name

        )

    # ==================================================
    # Emoji
    # ==================================================

    def set_emoji(

        self,

        emoji

    ):

        self.emoji = emoji

        if self.image is None:

            self.avatar.configure(

                text=emoji

            )

    # ==================================================
    # Image
    # ==================================================

    def set_image(

        self,

        image

    ):

        self.image = image

        self.avatar.configure(

            image=image,

            text=""

        )

    def clear_image(

        self

    ):

        self.image = None

        self.avatar.configure(

            image=None,

            text=self.emoji

        )

    # ==================================================
    # Theme
    # ==================================================

    def apply_theme(

        self

    ):

        self.avatar.configure(

            fg_color=self.theme.colors.surface,

            text_color=self.theme.colors.text

        )

        self.name_label.configure(

            text_color=self.theme.colors.secondary_text

        )

    # ==================================================
    # Helpers
    # ==================================================

    def data(

        self

    ):

        return {

            "name":

                self.name,

            "status":

                self.status,

            "emoji":

                self.emoji

        }