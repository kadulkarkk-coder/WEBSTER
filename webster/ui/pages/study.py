"""
WEBSTER Study Hub Page
=======================
Study tools: notes, PDF, flashcards, quiz, planner.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme


class StudyPage(ctk.CTkFrame):
    """Study hub with all study tools."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="📚  Study Hub",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(15, 5))

        grid = ctk.CTkScrollableFrame(self, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="nsew", padx=25, pady=10)
        grid.grid_columnconfigure((0, 1), weight=1)

        tools = [
            ("📝", "Notes", "Write & manage notes with AI", WebsterTheme.CYAN),
            ("📄", "PDF Reader", "Read and analyze PDFs", WebsterTheme.PURPLE),
            ("🃏", "Flashcards", "Create study flashcards", WebsterTheme.PINK),
            ("❓", "Quiz Generator", "Generate practice quizzes", WebsterTheme.ONLINE),
            ("📋", "Study Planner", "Plan your study sessions", WebsterTheme.CYAN),
            ("📊", "Progress", "Track your study progress", WebsterTheme.PURPLE),
        ]

        for i, (icon, title, desc, color) in enumerate(tools):
            card = ctk.CTkFrame(
                grid, fg_color=WebsterTheme.GLASS_BG,
                corner_radius=WebsterTheme.BORDER_RADIUS_LG,
                border_width=1, border_color=WebsterTheme.GLASS_BORDER
            )
            card.grid(row=i // 2, column=i % 2, sticky="nsew", padx=8, pady=8)

            ctk.CTkLabel(card, text=icon, font=(WebsterTheme.FONT_FAMILY, 28)).pack(anchor="w", padx=15, pady=(15, 2))
            ctk.CTkLabel(card, text=title, font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_LG, "bold"),
                         text_color=WebsterTheme.TEXT_PRIMARY).pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=desc, font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                         text_color=WebsterTheme.TEXT_MUTED).pack(anchor="w", padx=15, pady=(2, 15))
