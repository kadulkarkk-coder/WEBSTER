import customtkinter as ctk

from aura import plugins
from aura.ui import page_manager
from aura.ui.pages import memory, settings


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, page_manager):

        super().__init__(master, width=220)

        self.grid_rowconfigure(10, weight=1)

        study = ctk.CTkButton(
            self,
            text="📚 Study Hub",
            height=45,
            command=lambda: page_manager.show_page("study")
        )

        study.pack(fill="x", padx=15, pady=10)


        plugins = ctk.CTkButton(
            self,
            text="🔌 Plugins",
            height=45,
            command=lambda: page_manager.show_page("plugins")
        )

        plugins.pack(fill="x", padx=15, pady=10)


        memory = ctk.CTkButton(
            self,
            text="🧠 Memory",
            height=45,
            command=lambda: page_manager.show_page("memory")
        )

        memory.pack(fill="x", padx=15, pady=10)


        settings = ctk.CTkButton(
            self,
            text="⚙ Settings",
            height=45,
            command=lambda: page_manager.show_page("settings")
        )

        settings.pack(fill="x", padx=15, pady=10)