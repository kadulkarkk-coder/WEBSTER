"""
WEBSTER Desktop Application
=============================
Main application container with glassmorphism dark UI.
"""

import customtkinter as ctk
from typing import Any, Optional

from webster.config.branding import APP_NAME, VERSION, AI_NAME
from webster.ui.themes import WebsterTheme


class WebsterApp(ctk.CTk):
    """Main WEBSTER desktop application window."""

    def __init__(self, helvac=None, spidey=None, events=None):
        super().__init__()
        
        self.helvac = helvac
        self.spidey = spidey
        self.events = events
        
        # Window setup
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("1400x900")
        self.minsize(1100, 700)
        self.configure(fg_color=WebsterTheme.BG_DARK)
        
        # State
        self._current_page = "chat"
        self._sidebar_visible = True
        
        # Build UI
        self._build_layout()
        
        # Bind events
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind("<Configure>", self._on_resize)
        
        self.after(100, self._post_init)

    def _build_layout(self):
        """Build the main UI layout."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        from webster.ui.sidebar import WebsterSidebar
        self.sidebar = WebsterSidebar(self, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Main content area
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=2)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        
        # Pages container
        self.pages = {}
        self._create_pages()
        
        # Floating orb (always on top overlay)
        self._create_orb()

    def _create_pages(self):
        """Create all application pages."""
        from webster.ui.pages.chat import ChatPage
        from webster.ui.pages.study import StudyPage
        from webster.ui.pages.settings import SettingsPage
        from webster.ui.pages.dashboard import DashboardPage
        from webster.ui.pages.memory import MemoryPage
        from webster.ui.pages.calendar import CalendarPage
        from webster.ui.pages.plugins import PluginsPage
        
        self.pages = {
            "chat": ChatPage(self.content, self),
            "dashboard": DashboardPage(self.content, self),
            "study": StudyPage(self.content, self),
            "memory": MemoryPage(self.content, self),
            "calendar": CalendarPage(self.content, self),
            "plugins": PluginsPage(self.content, self),
            "settings": SettingsPage(self.content, self),
        }
        
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
        
        self._show_page("chat")

    def _create_orb(self):
        """Create the floating Spidey orb overlay."""
        from webster.ui.orb.orb_widget import SpideyOrbWidget
        self.orb = SpideyOrbWidget(self)
        self.orb.place(relx=0.95, rely=0.92, anchor="se")

    def _post_init(self):
        """Post-initialization tasks."""
        if self.spidey:
            self.spidey.set_ui_callback(self._on_spidey_message)
        self._update_status("Ready")

    def _on_spidey_message(self, message: str):
        """Handle incoming Spidey messages."""
        chat_page = self.pages.get("chat")
        if chat_page:
            chat_page.add_message("assistant", message)

    def _show_page(self, page_name: str):
        """Switch to a page."""
        if page_name in self.pages:
            self.pages[page_name].tkraise()
            self._current_page = page_name

    def _update_status(self, text: str):
        """Update status display."""
        if self.sidebar:
            self.sidebar.set_status(text)

    def _on_resize(self, event=None):
        """Handle window resize."""
        pass

    def _on_close(self):
        """Graceful shutdown."""
        if self.spidey:
            self.spidey.shutdown()
        self.destroy()

    # Navigation API
    def go_chat(self):
        self._show_page("chat")

    def go_dashboard(self):
        self._show_page("dashboard")

    def go_study(self):
        self._show_page("study")

    def go_memory(self):
        self._show_page("memory")

    def go_calendar(self):
        self._show_page("calendar")

    def go_plugins(self):
        self._show_page("plugins")

    def go_settings(self):
        self._show_page("settings")

    def toggle_sidebar(self):
        self._sidebar_visible = not self._sidebar_visible
        self.sidebar.grid_remove() if not self._sidebar_visible else self.sidebar.grid()

    def send_to_spidey(self, message: str):
        """Send user message to Spidey."""
        if self.spidey:
            self.spidey.process_message(message)

    def run(self):
        """Start the application main loop."""
        self.mainloop()
