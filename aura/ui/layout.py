from aura.ui.sidebar import Sidebar
from aura.ui.header import Header
from aura.ui.statusbar import StatusBar

from aura.ui.page_manager import PageManager

from aura.ui.home import Home

from aura.ui.pages.study_hub import StudyHub
from aura.ui.pages.plugins import PluginsPage
from aura.ui.pages.memory import MemoryPage
from aura.ui.pages.settings import SettingsPage


class Layout:

    def __init__(self, root):

        self.root = root

    def build(self):

        # Window Grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # ------------------------
        # Page Manager
        # ------------------------

        page_manager = PageManager(self.root)
        from aura.controller.aura_controller import AURAController
        controller = AURAController(page_manager)

        # ------------------------
        # Create Pages
        # ------------------------

        home = Home(self.root)

        study = StudyHub(self.root)

        plugins = PluginsPage(self.root)

        memory = MemoryPage(self.root)

        settings = SettingsPage(self.root)

        # ------------------------
        # Register Pages
        # ------------------------

        page_manager.register_page("home", home)
        page_manager.register_page("study", study)
        page_manager.register_page("plugins", plugins)
        page_manager.register_page("memory", memory)
        page_manager.register_page("settings", settings)

        # ------------------------
        # Sidebar
        # ------------------------

        sidebar = Sidebar(
            self.root,
            controller
        )

        sidebar.grid(
            row=0,
            column=0,
            rowspan=3,
            sticky="ns"
        )

        # ------------------------
        # Header
        # ------------------------

        header = Header(self.root)

        header.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        # ------------------------
        # Status Bar
        # ------------------------

        status = StatusBar(self.root)

        status.grid(
            row=2,
            column=1,
            sticky="ew"
        )

        # ------------------------
        # Default Page
        # ------------------------

        page_manager.show_page("home")