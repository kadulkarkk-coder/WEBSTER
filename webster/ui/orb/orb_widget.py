"""
Spidey Floating Orb Widget
===========================
A floating overlay orb that shows Spidey's status and provides quick access.
"""

import customtkinter as ctk
import threading
from webster.ui.themes import WebsterTheme


class SpideyOrbWidget(ctk.CTkFrame):
    """Floating interactive orb showing Spidey's status."""

    STATUS_COLORS = {
        "idle": WebsterTheme.CYAN_DIM,
        "listening": WebsterTheme.CYAN,
        "thinking": WebsterTheme.PURPLE,
        "speaking": WebsterTheme.PINK,
        "error": WebsterTheme.OFFLINE,
        "processing": WebsterTheme.PURPLE_DIM,
    }

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            width=60,
            height=60,
            **kwargs
        )
        self._status = "idle"
        self._expanded = False
        self._build()

    def _build(self):
        # Orb button
        self.orb_btn = ctk.CTkButton(
            self,
            text="🕷️",
            width=60,
            height=60,
            font=(WebsterTheme.FONT_FAMILY, 24),
            fg_color=WebsterTheme.GLASS_BG,
            hover_color=WebsterTheme.GLASS_HOVER,
            corner_radius=30,
            border_width=2,
            border_color=self.STATUS_COLORS[self._status],
            command=self._toggle_menu
        )
        self.orb_btn.pack()

        # Quick action menu (hidden by default)
        self.menu_frame = ctk.CTkFrame(
            self,
            fg_color=WebsterTheme.BG_MID,
            corner_radius=WebsterTheme.BORDER_RADIUS_MD,
            border_width=1,
            border_color=WebsterTheme.GLASS_BORDER
        )

        actions = [
            ("🎤", "Voice", self._action_voice),
            ("💬", "Chat", self._action_chat),
            ("📝", "Note", self._action_note),
            ("⚡", "Quick", self._action_quick),
        ]

        for icon, label, cmd in actions:
            btn = ctk.CTkButton(
                self.menu_frame,
                text=f"{icon} {label}",
                font=(WebsterTheme.FONT_FAMILY, 12),
                fg_color="transparent",
                hover_color=WebsterTheme.GLASS_HOVER,
                text_color=WebsterTheme.TEXT_SECONDARY,
                anchor="w",
                height=30,
                command=cmd
            )
            btn.pack(fill="x", padx=5, pady=2)

    def set_status(self, status: str):
        """Update the orb's status color."""
        if status in self.STATUS_COLORS:
            self._status = status
            self.orb_btn.configure(
                border_color=self.STATUS_COLORS[status]
            )
            self.after(100, self._pulse)

    def _pulse(self):
        """Subtle pulse animation on status change."""
        current = self.orb_btn.cget("fg_color")
        status_color = self.STATUS_COLORS.get(self._status, WebsterTheme.GLASS_BG)
        self.orb_btn.configure(fg_color=status_color)
        self.after(300, lambda: self.orb_btn.configure(fg_color=WebsterTheme.GLASS_BG))

    def _toggle_menu(self):
        """Show/hide quick action menu."""
        if self._expanded:
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack(pady=(5, 0))
        self._expanded = not self._expanded

    def _action_voice(self):
        self._toggle_menu()
        print("[Spidey Orb] Voice toggle")

    def _action_chat(self):
        self._toggle_menu()
        # Focus chat window
        master = self.winfo_toplevel()
        if hasattr(master, 'go_chat'):
            master.go_chat()

    def _action_note(self):
        self._toggle_menu()
        print("[Spidey Orb] Quick note")

    def _action_quick(self):
        self._toggle_menu()
        print("[Spidey Orb] Quick command")
