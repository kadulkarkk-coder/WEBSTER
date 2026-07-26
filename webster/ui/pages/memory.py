"""
WEBSTER Memory Page
===================
View and manage WEBSTER's memory and conversation history.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme
from webster.config.branding import AI_NAME


class MemoryPage(ctk.CTkFrame):
    """Memory and conversation history view."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._build()

    def _build(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="🧠  Memory",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(15, 5))

        # Stats bar
        stats = ctk.CTkFrame(self, fg_color=WebsterTheme.GLASS_BG,
                            corner_radius=WebsterTheme.BORDER_RADIUS_MD)
        stats.grid(row=1, column=0, sticky="ew", padx=25, pady=10)
        
        for label, value, color in [
            ("Conversations", "47", WebsterTheme.CYAN),
            ("Memories", "892", WebsterTheme.PURPLE),
            ("Context Size", "2.4K tokens", WebsterTheme.PINK),
            ("Last Saved", "Just now", WebsterTheme.ONLINE)
        ]:
            item = ctk.CTkFrame(stats, fg_color="transparent")
            item.pack(side="left", expand=True, fill="x", padx=10, pady=10)
            ctk.CTkLabel(item, text=value, font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XL, "bold"),
                        text_color=color).pack()
            ctk.CTkLabel(item, text=label, font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                        text_color=WebsterTheme.TEXT_MUTED).pack()

        # Conversation list
        conv_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        conv_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=10)
        conv_frame.grid_columnconfigure(0, weight=1)

        for i in range(10):
            item = ctk.CTkFrame(conv_frame, fg_color=WebsterTheme.GLASS_BG,
                               corner_radius=WebsterTheme.BORDER_RADIUS_MD,
                               border_width=1, border_color=WebsterTheme.GLASS_BORDER)
            item.pack(fill="x", pady=4)
            
            ctk.CTkLabel(item, text=f"Conversation #{47-i}",
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD, "bold"),
                        text_color=WebsterTheme.TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(8, 2))
            ctk.CTkLabel(item, text=f"Last message: How can I help you today?",
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                        text_color=WebsterTheme.TEXT_MUTED).pack(anchor="w", padx=15, pady=(0, 8))
