import customtkinter as ctk

from aura.ui.layout import Layout
from aura.theme.theme import Theme


class MainWindow(

    ctk.CTk

):

    """
    ==================================================

                    WEBSTER

                 Main Window

    Sprint 22

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        services

    ):

        super().__init__()

        self.services = services

        self.layout = None

        self.setup_window()

        self.build()

        self.bind_events()

    # ==================================================
    # Window Setup
    # ==================================================

    def setup_window(

        self

    ):

        self.title(

            "WEBSTER"

        )

        self.geometry(

            "1600x900"

        )

        self.minsize(

            1280,

            720

        )

        self.configure(

            fg_color=Theme.Colors.BACKGROUND

        )

        self.protocol(

            "WM_DELETE_WINDOW",

            self.on_close

        )

        self.grid_rowconfigure(

            0,

            weight=1

        )

        self.grid_columnconfigure(

            0,

            weight=1

        )

    # ==================================================
    # Build
    # ==================================================

    def build(

        self

    ):

        self.layout = Layout(

            self,

            self

        )

        self.layout.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

    # ==================================================
    # Navigation
    # ==================================================

    def show_page(

        self,

        page

    ):

        self.layout.show_page(

            page

        )


    def go_chat(

        self

    ):

        self.show_page(

            "chat"

        )


    def go_study(

        self

    ):

        self.show_page(

            "study"

        )


    def go_memory(

        self

    ):

        self.show_page(

            "memory"

        )


    def go_calendar(

        self

    ):

        self.show_page(

            "calendar"

        )


    def go_news(

        self

    ):

        self.show_page(

            "news"

        )


    def go_plugins(

        self

    ):

        self.show_page(

            "plugins"

        )


    def go_settings(

        self

    ):

        self.show_page(

            "settings"

        )

    # ==================================================
    # Events
    # ==================================================

    def bind_events(

        self

    ):

        self.bind(

            "<Configure>",

            self.on_resize

        )

    # ==================================================
    # Resize
    # ==================================================

    def on_resize(

        self,

        event

    ):

        if self.layout:

            self.layout.on_resize(

                event

            )

    # ==================================================
    # Services
    # ==================================================

    def service(

        self,

        name,

        default=None

    ):

        if hasattr(

            self.services,

            "get"

        ):

            return self.services.get(

                name,

                default

            )

        return default
    
    # ==================================================
    # Chat
    # ==================================================

    def send_message(

        self,

        message

    ):

        worker = self.service(

            "ai_worker"

        )

        if worker:

            worker.send(

                message

            )

    # ==================================================
    # Status
    # ==================================================

    def update_status(

        self,

        text

    ):

        chat = self.layout.page(

            "chat"

        )

        if chat:

            chat.title.set_subtitle(

                text

            )

    # ==================================================
    # Close
    # ==================================================

    def on_close(

        self

    ):

        self.destroy()

