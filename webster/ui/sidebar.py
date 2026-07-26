"""
WEBSTER Sidebar
=================
Collapsible sidebar with glassmorphism design.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme
from webster.config.branding import APP_NAME, VERSION, AI_NAME


class WebsterSidebar(ctk.CTkFrame):
    """Main navigation sidebar with WEBSTER branding."""

    NAV_ITEMS = [
        ("chat", "💬", "Chat", "main"),
        ("dashboard", "📊", "Dashboard", "main"),
        ("study", "📚", "Study Hub", "main"),
        ("memory", "🧠", "Memory", "main"),
        ("calendar", "📅", "Calendar", "main"),
        ("plugins", "🔌", "Plugins", "main"),
        ("settings", "⚙️", "Settings", "bottom"),
    ]

    def __init__(self, master, controller, **kwargs):
        super().__init__(
            master,
            fg_color=WebsterTheme.SIDEBAR_BG,
            width=WebsterTheme.SIDEBAR_WIDTH,
            corner_radius=0,
            **kwargs
        )
        self.controller = controller
        self._buttons = {}
        self._current = None
        
        self._build()
        self.set_active("chat")

    def _build(self):
        """Build sidebar layout."""
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self._build_header()
        
        # Separator
        ctk.CTkFrame(self, height=1, fg_color=WebsterTheme.GLASS_BORDER).grid(
            row=1, column=0, sticky="ew", padx=20, pady=(0, 10)
        )
        
        # Navigation scrollable frame
        self.nav_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", scrollbar_button_color=WebsterTheme.GLASS_BORDER,
            scrollbar_button_hover_color=WebsterTheme.TEXT_MUTED
        )
        self.nav_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 10))
        self.nav_frame.grid_columnconfigure(0, weight=1)
        
        # Build navigation items
        for key, icon, label, group in self.NAV_ITEMS:
            self._add_nav_button(key, icon, label, group)
        
        # Bottom section
        self._build_bottom()

    def _build_header(self):
        """Build the branded header."""
        header = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)
        
        # App name
        ctk.CTkLabel(
            header,
            text=APP_NAME,
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.CYAN
        ).pack(anchor="w")
        
        # Subtitle
        ctk.CTkLabel(
            header,
            text=f"{AI_NAME} Assistant",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
            text_color=WebsterTheme.TEXT_MUTED
        ).pack(anchor="w")

    def _add_nav_button(self, key: str, icon: str, label: str, group: str):
        """Add a navigation button."""
        frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        
        btn = ctk.CTkButton(
            frame,
            text=f"{icon}  {label}",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
            fg_color="transparent",
            text_color=WebsterTheme.TEXT_SECONDARY,
            hover_color=WebsterTheme.SIDEBAR_ITEM_HOVER,
            anchor="w",
            height=40,
            corner_radius=WebsterTheme.BORDER_RADIUS_MD,
            command=lambda k=key: self._navigate(k)
        )
        btn.pack(fill="x")
        self._buttons[key] = btn

    def _build_bottom(self):
        """Build bottom status section."""
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=3, column=0, sticky="ew", padx=15, pady=(5, 15))
        
        ctk.CTkFrame(bottom, height=1, fg_color=WebsterTheme.GLASS_BORDER).pack(
            fill="x", pady=(0, 10)
        )
        
        # Status indicator
        status_frame = ctk.CTkFrame(bottom, fg_color="transparent")
        status_frame.pack(fill="x")
        
        self.status_dot = ctk.CTkLabel(
            status_frame, text="●", text_color=WebsterTheme.ONLINE,
            font=(WebsterTheme.FONT_FAMILY, 10)
        )
        self.status_dot.pack(side="left", padx=(0, 5))
        
        self.status_label = ctk.CTkLabel(
            status_frame, text="Spidey Online",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
            text_color=WebsterTheme.TEXT_MUTED
        )
        self.status_label.pack(side="left")
        
        # Version
        ctk.CTkLabel(
            bottom, text=f"v{VERSION}",
            font=(WebsterTheme.FONT_FAMILY, 10),
            text_color=WebsterTheme.TEXT_MUTED
        ).pack(anchor="w", pady=(5, 0))

    def _navigate(self, key: str):
        """Handle navigation click."""
        self.set_active(key)
        if hasattr(self.controller, f"go_{key}"):
            getattr(self.controller, f"go_{key}")()
        elif key == "chat":
            self.controller.go_chat()
        elif key == "dashboard":
            self.controller.go_dashboard()

    def set_active(self, key: str):
        """Highlight active nav button."""
        if self._current and self._current in self._buttons:
            self._buttons[self._current].configure(
                fg_color="transparent",
                text_color=WebsterTheme.TEXT_SECONDARY
            )
        if key in self._buttons:
            self._buttons[key].configure(
                fg_color=WebsterTheme.SIDEBAR_ITEM_ACTIVE,
                text_color=WebsterTheme.CYAN
            )
            self._current = key

    def set_status(self, text: str):
        """Update status text."""
        self.status_label.configure(text=text)
