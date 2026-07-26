"""
WEBSTER Calendar Page
=====================
Calendar, reminders, and task management.
"""

import customtkinter as ctk
from webster.ui.themes import WebsterTheme


class CalendarPage(ctk.CTkFrame):
    """Calendar and task management."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self, text="📅  Calendar",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XXL, "bold"),
            text_color=WebsterTheme.TEXT_PRIMARY
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=25, pady=(15, 5))

        # Left: Calendar placeholder
        cal_frame = ctk.CTkFrame(self, fg_color=WebsterTheme.GLASS_BG,
                                 corner_radius=WebsterTheme.BORDER_RADIUS_LG,
                                 border_width=1, border_color=WebsterTheme.GLASS_BORDER)
        cal_frame.grid(row=1, column=0, sticky="nsew", padx=(25, 10), pady=10)
        cal_frame.grid_rowconfigure(0, weight=1)
        cal_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(cal_frame, text="🗓️  June 2025",
                     font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XL, "bold"),
                     text_color=WebsterTheme.TEXT_PRIMARY).pack(pady=20)

        days_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        days_frame.pack(pady=10)
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            ctk.CTkLabel(days_frame, text=day, width=40,
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                        text_color=WebsterTheme.TEXT_MUTED).pack(side="left")

        ctk.CTkLabel(cal_frame, text="Calendar integration coming soon",
                     font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
                     text_color=WebsterTheme.TEXT_MUTED).pack(pady=30)

        # Right: Tasks
        tasks_frame = ctk.CTkFrame(self, fg_color=WebsterTheme.GLASS_BG,
                                   corner_radius=WebsterTheme.BORDER_RADIUS_LG,
                                   border_width=1, border_color=WebsterTheme.GLASS_BORDER)
        tasks_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 25), pady=10)

        ctk.CTkLabel(tasks_frame, text="📋  Today's Tasks",
                     font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XL, "bold"),
                     text_color=WebsterTheme.TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15, 10))

        tasks = [
            ("Review flashcards", "Study", WebsterTheme.PURPLE, True),
            ("Read AI paper", "Research", WebsterTheme.CYAN, False),
            ("Plan project", "Work", WebsterTheme.PINK, False),
            ("Write notes", "Study", WebsterTheme.ONLINE, True),
        ]

        for task, category, color, done in tasks:
            item = ctk.CTkFrame(tasks_frame, fg_color="transparent")
            item.pack(fill="x", padx=15, pady=4)
            
            ctk.CTkCheckBox(item, text="", onvalue=True, offvalue=False,
                           fg_color=color, hover_color=color,
                           checkbox_height=20, checkbox_width=20
            ).pack(side="left", padx=(0, 10))
            
            ctk.CTkLabel(item, text=task,
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
                        text_color=WebsterTheme.TEXT_PRIMARY if not done else WebsterTheme.TEXT_MUTED
            ).pack(side="left")
            
            ctk.CTkLabel(item, text=category,
                        font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
                        text_color=color
            ).pack(side="right")
