import customtkinter as ctk

from aura.ui.header import Header
from aura.ui.sidebar import Sidebar

from aura.ui.pages.chat import ChatPage
from aura.ui.pages.study_hub import StudyHub
from aura.ui.pages.memory import MemoryPage
from aura.ui.pages.calendar import CalendarPage
from aura.ui.pages.news import NewsPage
from aura.ui.pages.plugins import PluginsPage
from aura.ui.pages.settings import SettingsPage


class Layout(

    ctk.CTkFrame

):

    """
    ==================================================

                    WEBSTER Layout

    Main UI Container

    Window

        Header
        Sidebar
        Content

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

            **kwargs

        )

        self.controller = controller

        self.pages = {}

        self.current_page = None

        self.build()

    # ==================================================
    # Build
    # ==================================================

    def build(

        self

    ):

        self.grid_rowconfigure(

            1,

            weight=1

        )

        self.grid_columnconfigure(

            1,

            weight=1

        )

        self._create_header()

        self._create_sidebar()

        self._create_container()

        self._create_pages()

        self.show_page(

            "chat"

        )

    # ==================================================
    # Header
    # ==================================================

    def _create_header(

        self

    ):

        self.header = Header(

            self,

            self.controller

        )

        self.header.grid(

            row=0,

            column=0,

            columnspan=2,

            sticky="ew"

        )

    # ==================================================
    # Sidebar
    # ==================================================

    def _create_sidebar(

        self

    ):

        self.sidebar = Sidebar(

            self,

            self.controller

        )

        self.sidebar.grid(

            row=1,

            column=0,

            sticky="ns"

        )

    # ==================================================
    # Content Container
    # ==================================================

    def _create_container(

        self

    ):

        self.container = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.container.grid(

            row=1,

            column=1,

            sticky="nsew",

            padx=(5,15),

            pady=(5,10)

        )

        self.container.grid_rowconfigure(

            0,

            weight=1

        )

        self.container.grid_columnconfigure(

            0,

            weight=1

        )

    # ==================================================
    # Create Pages
    # ==================================================

    def _create_pages(

        self

    ):

        self.pages = {

            "chat": ChatPage(

                self.container,

                self.controller

            ),

            "study": StudyHub(

                self.container,

                self.controller

            ),

            "memory": MemoryPage(

                self.container,

                self.controller

            ),

            "calendar": CalendarPage(

                self.container,

                self.controller

            ),

            "news": NewsPage(

                self.container,

                self.controller

            ),

            "plugins": PluginsPage(

                self.container,

                self.controller

            ),

            "settings": SettingsPage(

                self.container,

                self.controller

            )

        }

        for page in self.pages.values():

            page.grid(

                row=0,

                column=0,

                sticky="nsew"

            )

    # ==================================================
    # Current Page
    # ==================================================

    def get_current_page(

        self

    ):

        return self.current_page
    
    # ==================================================
    # Refresh Current
    # ==================================================

    def refresh(

        self

    ):

        if hasattr(

            self.current_page,

            "refresh"

        ):

            self.current_page.refresh()

    # ==================================================
    # Resize Event
    # ==================================================

    def on_resize(

        self,

        event=None

    ):

        if hasattr(

            self.current_page,

            "on_resize"

        ):

            self.current_page.on_resize(

                event

            )

    # ==================================================
    # Public API
    # ==================================================

    def header_widget(

        self

    ):

        return self.header


    def sidebar_widget(

        self

    ):

        return self.sidebar


    def container_widget(

        self

    ):

        return self.container


    def page(

        self,

        name

    ):

        return self.pages.get(

            name

        )

