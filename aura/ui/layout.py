from aura.ui.sidebar import Sidebar
from aura.ui.header import Header
from aura.ui.statusbar import StatusBar
from aura.ui.page_manager import PageManager

from aura.controller.aura_controller import AURAController

from aura.ui.pages.chat import ChatPage
from aura.ui.pages.study_hub import StudyHub
from aura.ui.pages.plugins import PluginsPage
from aura.ui.pages.memory import MemoryPage
from aura.ui.pages.settings import SettingsPage


class Layout:

    def __init__(

        self,

        root,

        services

    ):

        self.root = root

        self.services = services

        self.page_manager = None

        self.controller = None

    # -------------------------------------------------

    def build(self):

        self._configure_grid()

        self._create_controller()

        self._create_header()

        self._create_sidebar()

        self._create_pages()

        self._create_statusbar()

        self.page_manager.show_page("chat")

    # -------------------------------------------------

    def _configure_grid(self):

        self.root.grid_rowconfigure(1, weight=1)

        self.root.grid_columnconfigure(1, weight=1)

    # -------------------------------------------------

    def _create_controller(

        self

    ):

        self.page_manager = PageManager(

            self.root

        )

        self.controller = AURAController(

            self.page_manager,

            self.services

        )

    # -------------------------------------------------

    def _create_header(self):

        header = Header(self.root)

        header.grid(
            row=0,
            column=1,
            sticky="ew"
        )

    # -------------------------------------------------

    def _create_sidebar(self):

        sidebar = Sidebar(
            self.root,
            self.controller
        )

        sidebar.grid(
            row=0,
            column=0,
            rowspan=3,
            sticky="ns"
        )

    # -------------------------------------------------

    def _create_statusbar(self):

        status = StatusBar(self.root)

        status.grid(
            row=2,
            column=1,
            sticky="ew"
        )

    # -------------------------------------------------

    def _create_pages(self):

        chat = ChatPage(
            self.root,
            self.controller
        )

        study = StudyHub(self.root)

        plugins = PluginsPage(self.root)

        memory = MemoryPage(self.root)

        settings = SettingsPage(self.root)

        self.page_manager.register_page(
            "chat",
            chat
        )

        self.page_manager.register_page(
            "study",
            study
        )

        self.page_manager.register_page(
            "plugins",
            plugins
        )

        self.page_manager.register_page(
            "memory",
            memory
        )

        self.page_manager.register_page(
            "settings",
            settings
        )