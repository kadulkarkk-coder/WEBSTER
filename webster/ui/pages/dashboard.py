"""
WEBSTER Dashboard Page
=======================
Main dashboard showing system status, quick actions, and stats.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme
from webster.config.branding import AI_NAME


class DashboardPage(ctk.CTkFrame):
    """Main dashboard with cards and system overview."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.grid(row=0, column=0, sticky="ew", pady=(15, 5))
        ctk.CTkLabel(
            header, text="📊  Dashboard",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=25)

        # Dashboard grid
        grid = ctk.CTkScrollableFrame(self, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="nsew", padx=25, pady=10)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        cards = [
            ("🕷️", f"{AI_NAME} Status", "Online & Ready", WebsterTheme.ONLINE),
            ("💬", "Chats Today", "12 conversations", WebsterTheme.CYAN),
            ("📚", "Study Sessions", "3 today", WebsterTheme.PURPLE),
            ("🧠", "Memory Items", "247 stored", WebsterTheme.PINK),
            ("📅", "Upcoming", "2 reminders", WebsterTheme.ONLINE),
            ("⚡", "System", "All services OK", WebsterTheme.CYAN),
        ]

        for i, (icon, title, value, color) in enumerate(cards):
            card = self._create_card(grid, icon, title, value, color)
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=8, pady=8)

    def _create_card(self, parent, icon, title, value, color):
        card = ctk.CTkFrame(
            parent, fg_color=WebsterTheme.GLASS_BG,
            corner_radius=WebsterTheme.BORDER_RADIUS_LG,
            border_width=1, border_color=WebsterTheme.GLASS_BORDER,
            height=140
        )
        
        ctk.CTkLabel(
            card, text=icon,
            font=(WebsterTheme.FONT_FAMILY, 32)
        ).pack(anchor="w", padx=18, pady=(18, 5))

        ctk.CTkLabel(
            card, text=title,
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_LG, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).pack(anchor="w", padx=18)

        ctk.CTkLabel(
            card, text=value,
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
            text_color=color
        ).pack(anchor="w", padx=18, pady=(2, 18))

        return card
