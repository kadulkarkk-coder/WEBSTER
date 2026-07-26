"""
WEBSTER Settings Page
=====================
Application settings and configuration UI.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme


class SettingsPage(ctk.CTkFrame):
    """Application settings."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="⚙️  Settings",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(15, 5))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=25, pady=10)
        scroll.grid_columnconfigure(0, weight=1)

        sections = [
            ("🤖 AI Provider", [
                ("Provider", ctk.CTkOptionMenu, ["Gemini", "OpenAI", "Ollama"]),
                ("Temperature", ctk.CTkSlider, 0.7),
                ("Max Tokens", ctk.CTkEntry, "4096"),
            ]),
            ("🎤 Voice", [
                ("Wake Word", ctk.CTkSwitch, True),
                ("Auto-Listen", ctk.CTkSwitch, False),
                ("Speech Rate", ctk.CTkSlider, 1.0),
            ]),
            ("🎨 Appearance", [
                ("Theme", ctk.CTkOptionMenu, ["Dark", "Light", "System"]),
                ("Accent Color", ctk.CTkOptionMenu, ["Cyan", "Purple", "Pink"]),
            ]),
            ("🧠 Memory", [
                ("Auto-Save", ctk.CTkSwitch, True),
                ("Context Length", ctk.CTkOptionMenu, ["10", "25", "50", "100"]),
            ]),
            ("🔌 Integrations", [
                ("Web Dashboard", ctk.CTkSwitch, True),
                ("Mobile API", ctk.CTkSwitch, False),
                ("Cloud Sync", ctk.CTkSwitch, False),
            ]),
        ]

        for section_title, items in sections:
            frame = ctk.CTkFrame(
                scroll, fg_color=WebsterTheme.GLASS_BG,
                corner_radius=WebsterTheme.BORDER_RADIUS_LG,
                border_width=1, border_color=WebsterTheme.GLASS_BORDER
            )
            frame.pack(fill="x", pady=8, padx=5)
            
            ctk.CTkLabel(
                frame, text=section_title,
                font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_LG, "bold"),
                text_color=WebsterTheme.CYAN
            ).pack(anchor="w", padx=15, pady=(12, 8))

            for label, widget_type, default in items:
                row = ctk.CTkFrame(frame, fg_color="transparent")
                row.pack(fill="x", padx=15, pady=4)
                
                ctk.CTkLabel(
                    row, text=label,
                    font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
                    text_color=WebsterTheme.TEXT_SECONDARY
                ).pack(side="left")

                if widget_type == ctk.CTkSwitch:
                    widget_type(row, text="", onvalue=True, offvalue=False,
                               progress_color=WebsterTheme.CYAN,
                               button_color=WebsterTheme.CYAN if default else WebsterTheme.TEXT_MUTED
                    ).pack(side="right")
                elif widget_type == ctk.CTkOptionMenu:
                    widget_type(row, values=default, fg_color=WebsterTheme.BG_MID,
                               button_color=WebsterTheme.CYAN, text_color=WebsterTheme.TEXT_PRIMARY
                    ).pack(side="right")
                elif widget_type == ctk.CTkSlider:
                    widget_type(row, from_=0, to=1, number_of_steps=100,
                               progress_color=WebsterTheme.CYAN,
                               button_color=WebsterTheme.CYAN
                    ).pack(side="right", padx=(20, 0))
