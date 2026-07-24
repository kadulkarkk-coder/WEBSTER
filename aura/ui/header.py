import customtkinter as ctk

from aura.ui.widgets.glass_panel import GlassPanel
from aura.ui.widgets.glass_title import GlassTitle
from aura.ui.widgets.glass_button import GlassButton


class Header(

    ctk.CTkFrame

):

    """
    ==================================================

                    WEBSTER Header

    Sprint 22

        Cherry HUD
        Asset Driven
        Reusable

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        controller,

        **kwargs

    ):

        super().__init__(

            master,

            fg_color="transparent",

            height=95,

            **kwargs

        )

        self.controller = controller

        self.build()

import customtkinter as ctk

from aura.ui.widgets.glass_panel import GlassPanel
from aura.ui.widgets.glass_title import GlassTitle
from aura.ui.widgets.glass_button import GlassButton


class Header(

    ctk.CTkFrame

):

    """
    ==================================================

                    WEBSTER Header

    Sprint 22

        Cherry HUD
        Asset Driven
        Reusable

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        controller,

        **kwargs

    ):

        super().__init__(

            master,

            fg_color="transparent",

            height=95,

            **kwargs

        )

        self.controller = controller

        self.build()

    # ==================================================
    # Title
    # ==================================================

    def _build_title(

        self

    ):

        self.title = GlassTitle(

            self.panel.body(),

            title="WEBSTER",

            subtitle="Artificial Utilitarian Research Agent",

            icon_category="navigation",

            text="home"

        )

        self.title.pack(

            side="left",

            padx=20,

            pady=15

        )

    # ==================================================
    # Quick Actions
    # ==================================================

    def _build_actions(

        self

    ):

        self.actions = ctk.CTkFrame(

            self.panel.body(),

            fg_color="transparent"

        )

        self.actions.pack(

            side="right",

            padx=20

        )

        self.notifications = GlassButton(

            self.actions,

            panel="button_round",

            icon_category="system",

            text="bell",

            size=(50,50),

            command=self.on_notifications

        )

        self.notifications.pack(

            side="left",

            padx=6

        )

        self.notifications = GlassButton(

            self.actions,

            panel="button_round",

            icon_category="system",

            text="bell",

            size=(50,50),

            command=self.on_notifications

        )

        self.notifications.pack(

            side="left",

            padx=6

        )

        self.search = GlassButton(

            self.actions,

            panel="button_round",

            icon_category="system",

            text="search",

            size=(50,50),

            command=self.on_search

        )

        self.search.pack(

            side="left",

            padx=6

        )

        self.voice = GlassButton(

            self.actions,

            panel="button_round",

            icon_category="system",

            text="microphone",

            size=(50,50),

            command=self.on_voice

        )

        self.voice.pack(

            side="left",

            padx=6

        )

        self.settings = GlassButton(

            self.actions,

            panel="button_round",

            icon_category="system",

            text="settings",

            size=(50,50),

            command=self.on_settings

        )

        self.settings.pack(

            side="left",

            padx=6

        )

        self.profile = GlassButton(

            self.actions,

            panel="button_round",

            icon_category="system",

            text="profile",

            size=(50,50),

            command=self.on_profile

        )

        self.profile.pack(

            side="left",

            padx=(18,0)

        )

    # ==================================================
    # Events
    # ==================================================

    def on_notifications(

        self

    ):

        if hasattr(

            self.controller,

            "go_notifications"

        ):

            self.controller.go_notifications()

        else:

            print(

                "[HEADER] Notifications clicked."

            )


    def on_search(

        self

    ):

        if hasattr(

            self.controller,

            "focus_search"

        ):

            self.controller.focus_search()

        elif hasattr(

            self.controller,

            "go_chat"

        ):

            self.controller.go_chat()

        print(

            "[HEADER] Search activated."

        )


    def on_voice(

        self

    ):

        if hasattr(

            self.controller,

            "toggle_voice"

        ):

            self.controller.toggle_voice()

        print(

            "[HEADER] Voice assistant toggled."

        )


    def on_settings(

        self

    ):

        if hasattr(

            self.controller,

            "go_settings"

        ):

            self.controller.go_settings()


    def on_profile(

        self

    ):

        if hasattr(

            self.controller,

            "go_profile"

        ):

            self.controller.go_profile()

        else:

            print(

                "[HEADER] Profile clicked."

            )
