import customtkinter as ctk

from aura.ui.widgets.glass_panel import GlassPanel
from aura.ui.widgets.glass_nav_button import GlassNavButton
from aura.ui.widgets.glass_separator import GlassSeparator
from aura.ui.widgets.glass_title import GlassTitle


class Sidebar(

    ctk.CTkFrame

):

    """
    ==================================================

                    WEBSTER Sidebar

    Sprint 22

    Modern Cherry UI

    Asset Driven

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

            width=285,

            **kwargs

        )

        self.controller = controller

        self.buttons = {}

        self.current = None

        self.build()

    # ==================================================
    # Build
    # ==================================================

    def build(

        self

    ):

        self.grid_rowconfigure(

            0,

            weight=1

        )

        self.grid_columnconfigure(

            0,

            weight=1

        )

        self.panel = GlassPanel(

            self,

            image="panel_sidebar",

            size=(280,900)

        )

        self.panel.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=(10,8),

            pady=10

        )

        self._build_header()

        self._build_navigation()

        self._build_footer()

    # ==================================================
    # Header
    # ==================================================

    def _build_header(

        self

    ):

        self.header = GlassTitle(

            self.panel.body(),

            title="WEBSTER",

            subtitle="AI Operating System",

            icon_category="navigation",

            text="home"

        )

        self.header.pack(

            anchor="w",

            padx=20,

            pady=(25,15)

        )

        self.separator = GlassSeparator(

            self.panel.body(),

            orientation="horizontal",

            size=(220,2)

        )

        self.separator.pack(

            padx=18,

            pady=(0,20),

            fill="x"

        )

    # ==================================================
    # Navigation
    # ==================================================

    def _build_navigation(

        self

    ):

        self.navigation = ctk.CTkFrame(

            self.panel.body(),

            fg_color="transparent"

        )

        self.navigation.pack(

            fill="x",

            padx=14

        )

        self.pages = [

            (

                "chat",

                "Chat",

                "chat",

                self.controller.go_chat

            ),

            (

                "study",

                "Study Hub",

                "study",

                self.controller.go_study

            ),

            (

                "memory",

                "Memory",

                "memory",

                self.controller.go_memory

            ),

            (

                "calendar",

                "Calendar",

                "calendar",

                self.controller.go_calendar

            ),

            (

                "news",

                "Daily Brief",

                "news",

                self.controller.go_news

            ),

            (

                "plugins",

                "Plugins",

                "plugins",

                self.controller.go_plugins

            ),

            (

                "settings",

                "Settings",

                "settings",

                self.controller.go_settings

            )

        ]

        for page, title, text, callback in self.pages:

            button = GlassNavButton(

                self.navigation,

                text=title,

                icon_category="navigation",

                text=text,

                command=lambda p=page, c=callback:

                    self.navigate(

                        p,

                        c

                    )

            )

            button.pack(

                fill="x",

                pady=5

            )

            self.buttons[page] = button

        self.set_active(

            "chat"

        )

    # ==================================================
    # Navigation
    # ==================================================

    def navigate(

        self,

        page,

        callback

    ):

        self.set_active(

            page

        )

        if callable(

            callback

        ):

            callback()

    # ==================================================
    # Active Button
    # ==================================================

    def set_active(

        self,

        page

    ):

        if self.current == page:

            return

        if self.current in self.buttons:

            self.buttons[

                self.current

            ].set_active(

                False

            )

        if page in self.buttons:

            self.buttons[

                page

            ].set_active(

                True

            )

            self.current = page

    # ==================================================
    # Footer
    # ==================================================

    def _build_footer(

        self

    ):

        self.footer = ctk.CTkFrame(

            self.panel.body(),

            fg_color="transparent"

        )

        self.footer.pack(

            side="bottom",

            fill="x",

            padx=18,

            pady=(20,20)

        )

        GlassSeparator(

            self.footer,

            orientation="horizontal",

            size=(220,2)

        ).pack(

            fill="x",

            pady=(0,15)

        )

        self.status = GlassTitle(

            self.footer,

            title="ONLINE",

            subtitle="WEBSTER v0.22",

            icon_category="system",

            text="status"

        )

        self.status.pack(

            anchor="w"

        )

    # ==================================================
    # Public API
    # ==================================================

    def enable(

        self,

        page

    ):

        if page in self.buttons:

            self.buttons[

                page

            ].enable()

    def disable(

        self,

        page

    ):

        if page in self.buttons:

            self.buttons[

                page

            ].disable()

    def get_current(

        self

    ):

        return self.current

    def add_page(

        self,

        key,

        text,

        text,

        callback

    ):

        button = GlassNavButton(

            self.navigation,

            text=text,

            icon_category="navigation",

            text=text,

            command=lambda:

                self.navigate(

                    key,

                    callback

                )

        )

        button.pack(

            fill="x",

            pady=5

        )

        self.buttons[

            key

        ] = button

    def remove_page(

        self,

        key

    ):

        if key not in self.buttons:

            return

        self.buttons[

            key

        ].destroy()

        del self.buttons[

            key

        ]

