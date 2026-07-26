"""
WEBSTER Plugins Page
====================
Plugin management interface.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme


class PluginsPage(ctk.CTkFrame):
    """Plugin management."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="🔌  Plugins",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(15, 5))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=25, pady=10)
        scroll.grid_columnconfigure(0, weight=1)

        plugins = [
            ("📄", "PDF Reader", "Read and analyze PDF documents", "1.0.0", True),
            ("🌐", "Web Search", "Search the internet", "1.0.0", True),
            ("📝", "Notes", "AI-powered note taking", "1.0.0", True),
            ("🎨", "Image Gen", "Generate images from text", "1.0.0", False),
            ("📊", "Analytics", "Usage analytics and insights", "1.0.0", False),
            ("🔄", "Cloud Sync", "Sync across devices", "1.0.0", False),
        ]

        for icon, name, desc, version, enabled in plugins:
            item = ctk.CTkFrame(scroll, fg_color=WebsterTheme.GLASS_BG,
                               corner_radius=WebsterTheme.BORDER_RADIUS_MD,
                               border_width=1, border_color=WebsterTheme.GLASS_BORDER)
            item.pack(fill="x", pady=5)
            
            ctk.CTkLabel(item, text=f"{icon}  {name}",
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_LG, "bold"),
                        text_color=WebsterTheme.TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(item, text=desc,
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                        text_color=WebsterTheme.TEXT_MUTED).pack(anchor="w", padx=15)
            
            ctk.CTkLabel(item, text=f"v{version}",
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                        text_color=WebsterTheme.TEXT_MUTED
            ).pack(anchor="w", padx=15, pady=(0, 10))
