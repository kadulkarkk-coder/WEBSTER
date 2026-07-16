import customtkinter as ctk

from aura.ui.orb.orb_controller import OrbController


class ChatPage(ctk.CTkFrame):

    def __init__(self, master, controller):

        super().__init__(master)

        self.controller = controller

        self.build()

        self.orb_controller = OrbController(
            self.orb,
            self.status
        )

        self.load_history()

    # ==================================================
    # Build UI
    # ==================================================

    def build(self):

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ----------------------------------------------
        # Orb
        # ----------------------------------------------

        self.orb = ctk.CTkLabel(
            self,
            text="🔵",
            font=("Segoe UI Emoji", 46)
        )

        self.orb.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        # ----------------------------------------------
        # Status
        # ----------------------------------------------

        self.status = ctk.CTkLabel(
            self,
            text="How can I help you today?",
            font=("Segoe UI", 14)
        )

        self.status.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        # ----------------------------------------------
        # Chat Area
        # ----------------------------------------------

        self.chatbox = ctk.CTkTextbox(
            self,
            wrap="word"
        )

        self.chatbox.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20
        )

        self.chatbox.configure(
            state="disabled"
        )

        # ----------------------------------------------
        # Bottom Bar
        # ----------------------------------------------

        bottom = ctk.CTkFrame(self)

        bottom.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=20
        )

        bottom.grid_columnconfigure(
            0,
            weight=1
        )

        self.entry = ctk.CTkEntry(
            bottom,
            placeholder_text="Ask AURA anything..."
        )

        self.entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.entry.bind(
            "<Return>",
            self.on_enter
        )

        self.send_button = ctk.CTkButton(
            bottom,
            text="Send",
            width=90,
            command=self.send_message
        )

        self.send_button.grid(
            row=0,
            column=1
        )

    # ==================================================
    # Enter Key
    # ==================================================

    def on_enter(self, event=None):

        self.send_message()

    # ==================================================
    # Append Message
    # ==================================================

    def append_message(self, speaker, message):

        self.chatbox.configure(
            state="normal"
        )

        self.chatbox.insert(
            "end",
            f"{speaker}: {message}\n\n"
        )

        self.chatbox.configure(
            state="disabled"
        )

        self.chatbox.see("end")

    # ==================================================
    # Load History
    # ==================================================

    def load_history(self):

        memory = self.controller.get_service("memory")

        if memory is None:
            return

        messages = memory.get_messages()

        for message in messages:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            if role == "user":

                self.append_message(
                    "👤 You",
                    content
                )

            elif role == "assistant":

                self.append_message(
                    "🤖 AURA",
                    content
                )

    # ==================================================
    # Send Message
    # ==================================================

    def send_message(self):

        prompt = self.entry.get().strip()

        if not prompt:
            return

        self.entry.delete(
            0,
            "end"
        )

        self.append_message(
            "👤 You",
            prompt
        )

        self.orb_controller.thinking()

        self.update_idletasks()

        try:

            response = self.controller.send_message(
                prompt
            )

        except Exception as e:

            self.orb_controller.error()

            response = f"[ERROR] {e}"

        self.append_message(
            "🤖 AURA",
            response
        )

        self.orb_controller.idle()

        self.entry.focus()

    # ==================================================
    # Clear Chat
    # ==================================================

    def clear_chat(self):

        self.chatbox.configure(
            state="normal"
        )

        self.chatbox.delete(
            "1.0",
            "end"
        )

        self.chatbox.configure(
            state="disabled"
        )

    # ==================================================
    # Focus Entry
    # ==================================================

    def focus_input(self):

        self.entry.focus()