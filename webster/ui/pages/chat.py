"""
WEBSTER Chat Page
==================
Spidey chat interface with message history and voice button.
"""

import customtkinter as ctk
from datetime import datetime
from typing import Any, Dict, List, Optional

from webster.ui.themes import WebsterTheme
from webster.config.branding import AI_NAME


class ChatPage(ctk.CTkFrame):
    """Spidey AI Chat Interface."""

    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        self._messages: List[Dict] = []
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", height=50)
        header.grid(row=0, column=0, sticky="ew", pady=(10, 0))
        header.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(header, fg_color=WebsterTheme.GLASS_BG, corner_radius=WebsterTheme.BORDER_RADIUS_MD)
        inner.pack(expand=True, fill="x", padx=20)
        
        ctk.CTkLabel(
            inner,
            text=f"🕷️  {AI_NAME}",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_XL, "bold"),
            text_color=WebsterTheme.CYAN
        ).pack(side="left", padx=15, pady=8)
        
        ctk.CTkLabel(
            inner,
            text="Online",
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_SM),
            text_color=WebsterTheme.ONLINE
        ).pack(side="right", padx=15)

        # Messages area
        self.msg_container = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=WebsterTheme.GLASS_BORDER,
            scrollbar_button_hover_color=WebsterTheme.TEXT_MUTED
        )
        self.msg_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.msg_container.grid_columnconfigure(0, weight=1)

        # Welcome message
        self.add_message("assistant", f"Hi! I'm {AI_NAME}. How can I help you today? 🕷️")

        # Input area
        self._build_input_area()

    def _build_input_area(self):
        input_frame = ctk.CTkFrame(self, fg_color=WebsterTheme.GLASS_BG, corner_radius=WebsterTheme.BORDER_RADIUS_LG)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(5, 20))
        input_frame.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkTextbox(
            input_frame,
            height=45,
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
            fg_color="transparent",
            text_color=WebsterTheme.TEXT_PRIMARY,
            border_width=0,
            wrap="word"
        )
        self.input_box.grid(row=0, column=0, sticky="ew", padx=(15, 5), pady=8)
        self.input_box.bind("<Return>", self._on_enter)

        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=1, padx=(0, 8))

        # Voice button
        self.voice_btn = ctk.CTkButton(
            btn_frame,
            text="🎤",
            width=40,
            height=40,
            font=(WebsterTheme.FONT_FAMILY, 18),
            fg_color=WebsterTheme.GLASS_BG,
            hover_color=WebsterTheme.GLASS_HOVER,
            corner_radius=WebsterTheme.BORDER_RADIUS_MD,
            command=self._toggle_voice
        )
        self.voice_btn.pack(side="left", padx=2)

        # Send button
        ctk.CTkButton(
            btn_frame,
            text="➤",
            width=40,
            height=40,
            font=(WebsterTheme.FONT_FAMILY, 18),
            fg_color=WebsterTheme.CYAN,
            hover_color=WebsterTheme.CYAN_DIM,
            corner_radius=WebsterTheme.BORDER_RADIUS_MD,
            command=self._send_message
        ).pack(side="left")

    def add_message(self, role: str, content: str):
        """Add a message to the chat."""
        bubble = ctk.CTkFrame(
            self.msg_container,
            fg_color=WebsterTheme.CHAT_USER_BG if role == "user" else WebsterTheme.CHAT_AI_BG,
            corner_radius=WebsterTheme.CHAT_BORDER_RADIUS
        )
        bubble.grid(row=len(self._messages), column=0, sticky="e" if role == "user" else "w",
                    padx=(60 if role == "user" else 10, 10 if role == "user" else 60), pady=5)
        bubble.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            bubble,
            text=content,
            font=(WebsterTheme.FONT_FAMILY, WebsterTheme.FONT_SIZE_MD),
            text_color=WebsterTheme.TEXT_PRIMARY,
            wraplength=500,
            justify="left"
        ).pack(padx=15, pady=10)

        self._messages.append({"role": role, "content": content, "timestamp": datetime.now().isoformat()})
        self.msg_container._parent_canvas.yview_moveto(1.0)

    def _send_message(self):
        """Send user message to Spidey."""
        text = self.input_box.get("1.0", "end-1c").strip()
        if not text:
            return
        self.input_box.delete("1.0", "end")
        self.add_message("user", text)
        
        if self.controller:
            self.controller.send_to_spidey(text)

    def _toggle_voice(self):
        """Toggle voice input."""
        if hasattr(self.controller, 'spidey') and self.controller.spidey:
            self.controller.spidey.toggle_voice()

    def _on_enter(self, event):
        """Handle Enter key to send."""
        if not event.state & 0x1:  # Shift not pressed
            self._send_message()
            return "break"
