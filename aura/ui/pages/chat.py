import customtkinter as ctk

from aura.core.ai_worker import AIWorker
from aura.ui.orb.orb_controller import OrbController


class ChatPage(ctk.CTkFrame):

    """
    AURA Chat Interface

    Responsibilities
    ----------------
    • Display conversation
    • Send prompts
    • Stream AI responses
    • Update orb & status
    • Auto scrolling
    • Background AI worker
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(
        self,
        master,
        controller
    ):

        super().__init__(master)

        self.controller = controller

        self.build()

        self.orb_controller = OrbController(

            self.orb,

            self.status

        )

        self.update_status()
        
        self.entry.focus()

    # ==================================================
    # Build UI
    # ==================================================

    def build(self):

        # ----------------------------------------------
        # Layout
        # ----------------------------------------------

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------
        # Orb
        # ----------------------------------------------

        self.orb = ctk.CTkLabel(

            self,

            text="🔵",

            font=(
                "Segoe UI Emoji",
                46
            )

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

            text="Ready",

            font=(
                "Segoe UI",
                14
            )

        )

        self.status.grid(

            row=1,

            column=0,

            pady=(0, 10)

        )

        # ----------------------------------------------
        # Chat Container
        # ----------------------------------------------

        chat_frame = ctk.CTkFrame(
            self
        )

        chat_frame.grid(

            row=2,

            column=0,

            sticky="nsew",

            padx=20

        )

        chat_frame.grid_rowconfigure(
            0,
            weight=1
        )

        chat_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ----------------------------------------------
        # Chat Box
        # ----------------------------------------------

        self.chatbox = ctk.CTkTextbox(

            chat_frame,

            wrap="word",

            corner_radius=12

        )

        self.chatbox.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

        self.chatbox.configure(

            state="disabled"

        )

        # ----------------------------------------------
        # Scroll Buttons
        # ----------------------------------------------

        self.top_button = ctk.CTkButton(

            chat_frame,

            text="▲",

            width=38,

            command=self.scroll_to_top

        )

        self.top_button.place(

            relx=0.97,

            rely=0.84,

            anchor="center"

        )

        self.bottom_button = ctk.CTkButton(

            chat_frame,

            text="▼",

            width=38,

            command=self.scroll_to_bottom

        )

        self.bottom_button.place(

            relx=0.97,

            rely=0.92,

            anchor="center"

        )

        # ----------------------------------------------
        # Bottom Input Bar
        # ----------------------------------------------

        bottom = ctk.CTkFrame(
            self
        )

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

        # ----------------------------------------------
        # Message Entry
        # ----------------------------------------------

        self.entry = ctk.CTkEntry(

            bottom,

            placeholder_text="Ask WEBSTER anything..."

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

        # ----------------------------------------------
        # Send Button
        # ----------------------------------------------

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
    # Status
    # ==================================================

    def update_status(self):

        status_manager = self.controller.get_service(

            "status_manager"

        )

        if status_manager is None:

            return

        data = status_manager.get_status()

        self.status.configure(

            text=data["text"]

        )

        self.orb.configure(

            text=data["emoji"]

        )

        state = status_manager.get_status()

        if state == "idle":

            self.orb_controller.idle()

        elif state == "thinking":

            self.orb_controller.thinking()

        elif state == "listening":

            self.orb_controller.listening()

        elif state == "speaking":

            self.orb_controller.speaking()

        elif state == "error":

            self.orb_controller.error()

    # ==================================================
    # Append Message
    # ==================================================

    def append_message(
        self,
        speaker,
        message
    ):

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

        self.scroll_to_bottom()

    # ==================================================
    # Load Conversation History
    # ==================================================

    def load_history(self):

        memory = self.controller.get_service(
            "memory"
        )

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
                    "🕷️ WEBSTER",
                    content
                )

            elif role == "system":

                self.append_message(
                    "⚙ System",
                    content
                )

    # ==================================================
    # Scroll Helpers
    # ==================================================

    def scroll_to_top(self):

        self.chatbox.yview_moveto(
            0
        )

    # --------------------------------------------------

    def scroll_to_bottom(self):

        self.chatbox.see(
            "end"
        )

    # ==================================================
    # Keyboard
    # ==================================================

    def on_enter(
        self,
        event=None
    ):

        self.send_message()

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

        self.begin_stream()

        self.entry.configure(
            state="disabled"
        )

        self.send_button.configure(
            state="disabled"
        )

        status = self.controller.get_service(
            "status_manager"
        )

        if status:

            status.set_state(
                "thinking"
            )

        self.update_status()

        worker = self.controller.get_service(
            "ai_worker"
        )

        worker.start_stream(

            self.controller.stream_message,

            prompt

        )

        self.after(
            30,
            self.poll_stream
        )

    # ==================================================
    # Begin Streaming
    # ==================================================

    def begin_stream(self):

        self.chatbox.configure(
            state="normal"
        )

        self.chatbox.insert(
            "end",
            "🕷️ WEBSTER: "
        )

        self.chatbox.configure(
            state="disabled"
        )

        self.scroll_to_bottom()

    # ==================================================
    # Poll Worker Queue
    # ==================================================

    def poll_stream(self):

        worker = self.controller.get_service(
            "ai_worker"
        )

        while True:

            chunk = worker.get_chunk()

            if chunk is None:

                break

            if chunk is AIWorker.END:

                self.finish_stream()

                self.finish_ai()

                return

            if isinstance(
                chunk,
                Exception
            ):

                self.stream_chunk(

                    f"\n\n[ERROR]\n{chunk}"

                )

                self.finish_stream()

                self.finish_ai()

                return

            self.stream_chunk(
                chunk
            )

        self.after(

            30,

            self.poll_stream

        )

    # ==================================================
    # Stream One Chunk
    # ==================================================

    def stream_chunk(

        self,

        chunk

    ):

        self.chatbox.configure(

            state="normal"

        )

        self.chatbox.insert(

            "end",

            chunk

        )

        self.chatbox.configure(

            state="disabled"

        )

        self.scroll_to_bottom()

    # ==================================================
    # Finish Stream
    # ==================================================

    def finish_stream(self):

        self.chatbox.configure(

            state="normal"

        )

        self.chatbox.insert(

            "end",

            "\n\n"

        )

        self.chatbox.configure(

            state="disabled"

        )

        self.scroll_to_bottom()

    # ==================================================
    # Finish AI Request
    # ==================================================

    def finish_ai(self):

        status = self.controller.get_service(
            "status_manager"
        )

        if status:

            status.set_state(
                "idle"
            )

        self.update_status()

        self.entry.configure(
            state="normal"
        )

        self.send_button.configure(
            state="normal"
        )

        self.entry.focus()

    # ==================================================
    # Focus Input
    # ==================================================

    def focus_input(self):

        self.entry.focus()

    # ==================================================
    # Refresh Page
    # ==================================================

    def refresh(self):

        self.update_status()

    # ==================================================
    # Clear Display
    # ==================================================

    def clear_display(self):

        """
        Clears only the textbox.

        Memory is NOT deleted.
        """

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
    # Reload Conversation
    # ==================================================

    def reload_history(self):

        """
        Reload messages from MemoryService.
        """

        self.clear_display()

        self.load_history()

    # ==================================================
    # Destructor
    # ==================================================

    def destroy(self):

        super().destroy()