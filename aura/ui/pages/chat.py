import customtkinter as ctk

from aura.ui.widgets.glass_panel import GlassPanel
from aura.ui.widgets.glass_bar import GlassBar
from aura.ui.widgets.glass_entry import GlassEntry
from aura.ui.widgets.glass_button import GlassButton
from aura.ui.widgets.glass_ring import GlassRing
from aura.ui.widgets.glass_title import GlassTitle
from aura.ui.widgets.glass_separator import GlassSeparator
from aura.ui.widgets.glass_frame import GlassFrame


class ChatPage(

    ctk.CTkFrame

):

    """
    ==================================================

                    WEBSTER Chat

    Sprint 22

    Cherry Glass Interface

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        controller,

        **kwargs

    ):

        super().__init__(

            master,

            fg_color="transparent",

            **kwargs

        )

        self.controller = controller

        self.build()

    # ==================================================
    # Build
    # ==================================================

    def build(

        self

    ):

        self.grid_rowconfigure(

            0,

            weight=1

        )

        self.grid_rowconfigure(

            1,

            weight=0

        )

        self.grid_columnconfigure(

            0,

            weight=4

        )

        self.grid_columnconfigure(

            1,

            weight=1

        )

        self._build_chat_panel()

        self._build_ai_panel()

        self._build_input_bar()

    # ==================================================
    # Chat Panel
    # ==================================================

    def _build_chat_panel(

        self

    ):

        self.chat_panel = GlassPanel(

            self,

            image="panel_large",

            size=(980,720)

        )

        self.chat_panel.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=(15,8),

            pady=(10,8)

        )

        self.chat_panel.body().grid_rowconfigure(

            0,

            weight=1

        )

        self.chat_panel.body().grid_columnconfigure(

            0,

            weight=1

        )

        self.messages = ctk.CTkScrollableFrame(

            self.chat_panel.body(),

            fg_color="transparent"

        )

        self.messages.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=20,

            pady=20

        )

    # ==================================================
    # AI Panel
    # ==================================================

    def _build_ai_panel(

        self

    ):

        self.ai_panel = GlassPanel(

            self,

            image="panel_small",

            size=(320,720)

        )

        self.ai_panel.grid(

            row=0,

            column=1,

            sticky="nsew",

            padx=(8,15),

            pady=(10,8)

        )

        self.ai_panel.body().grid_columnconfigure(

            0,

            weight=1

        )

        self.ring = GlassRing(

            self.ai_panel.body(),

            state="idle",

            size=(180,180)

        )

        self.ring.pack(

            pady=(30,20)

        )

        self.title = GlassTitle(

            self.ai_panel.body(),

            title="WEBSTER",

            subtitle="Standing By",

            icon_category="system",

            text="ai"

        )

        self.title.pack(

            pady=(0,20)

        )

        GlassSeparator(

            self.ai_panel.body()

        ).pack(

            fill="x",

            padx=20,

            pady=(0,20)

        )

        self.info = GlassFrame(

            self.ai_panel.body(),

            image="frame_info",

            size=(260,320)

        )

        self.info.pack(

            padx=18,

            fill="both",

            expand=True
        )

    # ==================================================
    # Input Bar
    # ==================================================

    def _build_input_bar(

        self

    ):

        self.bottom_panel = GlassPanel(

            self,

            image="panel_bottom",

            size=(1320,110)

        )

        self.bottom_panel.grid(

            row=1,

            column=0,

            columnspan=2,

            sticky="ew",

            padx=15,

            pady=(0,10)

        )

        self.bottom_panel.body().grid_rowconfigure(

            0,

            weight=1

        )

        self.bottom_panel.body().grid_columnconfigure(

            1,

            weight=1

        )

        self._build_left_actions()

        self._build_entry()

        self._build_right_actions()

    # ==================================================
    # Left Actions
    # ==================================================

    def _build_left_actions(

        self

    ):

        self.left_actions = ctk.CTkFrame(

            self.bottom_panel.body(),

            fg_color="transparent"

        )

        self.left_actions.grid(

            row=0,

            column=0,

            padx=(15,10),

            pady=15,

            sticky="w"

        )

        self.voice_button = GlassButton(

            self.left_actions,

            panel="button_round",

            icon_category="system",

            text="voice",

            size=(56,56),

            command=self.toggle_voice

        )

        self.voice_button.pack(

            side="left",

            padx=4

        )

        self.mic_button = GlassButton(

            self.left_actions,

            panel="button_round",

            icon_category="system",

            text="microphone",

            size=(56,56),

            command=self.start_listening

        )

        self.mic_button.pack(

            side="left",

            padx=4

        )

        self.camera_button = GlassButton(

            self.left_actions,

            panel="button_round",

            icon_category="system",

            text="camera",

            size=(56,56),

            command=self.open_camera

        )

        self.camera_button.pack(

            side="left",

            padx=4

        )

    # ==================================================
    # Entry
    # ==================================================

    def _build_entry(

        self

    ):

        self.entry = GlassEntry(

            self.bottom_panel.body(),

            placeholder="Ask WEBSTER anything...",

            size=(780,60)

        )

        self.entry.grid(

            row=0,

            column=1,

            sticky="ew",

            padx=15,

            pady=15

        )

        self.entry.bind(

            "<Return>",

            self.on_enter

        )

    # ==================================================
    # Right Actions
    # ==================================================

    def _build_right_actions(

        self

    ):

        self.right_actions = ctk.CTkFrame(

            self.bottom_panel.body(),

            fg_color="transparent"

        )

        self.right_actions.grid(

            row=0,

            column=2,

            padx=(10,15),

            pady=15,

            sticky="e"

        )

        self.memory_button = GlassButton(

            self.right_actions,

            panel="button_round",

            icon_category="system",

            text="memory",

            size=(56,56),

            command=self.open_memory

        )

        self.memory_button.pack(

            side="left",

            padx=4

        )

        self.plugins_button = GlassButton(

            self.right_actions,

            panel="button_round",

            icon_category="system",

            text="plugins",

            size=(56,56),

            command=self.open_plugins

        )

        self.plugins_button.pack(

            side="left",

            padx=4

        )

        self.send_button = GlassButton(

            self.right_actions,

            panel="button_round",

            icon_category="controls",

            text="send",

            size=(60,60),

            command=self.send_message

        )

        self.send_button.pack(

            side="left",

            padx=(8,0)

        )

    # ==================================================
    # Send Message
    # ==================================================

    def send_message(

        self

    ):

        message = self.entry.get().strip()

        if not message:

            return

        self.entry.clear()

        self.append_message(

            sender="You",

            message=message

        )

        if hasattr(

            self.controller,

            "send_message"

        ):

            self.controller.send_message(

                message

            )

    # ==================================================
    # Enter
    # ==================================================

    def on_enter(

        self,

        event=None

    ):

        self.send_message()

        return "break"
    
    # ==================================================
    # Append Message
    # ==================================================

    def append_message(

        self,

        sender,

        message

    ):

        bubble = GlassFrame(

            self.messages,

            image="frame_message",

            size=(760,120)

        )

        bubble.pack(

            fill="x",

            padx=8,

            pady=6

        )

        title = ctk.CTkLabel(

            bubble.body(),

            text=sender,

            anchor="w",

            font=(

                "Segoe UI",

                14,

                "bold"

            )

        )

        title.pack(

            anchor="w",

            padx=15,

            pady=(12,4)

        )

        body = ctk.CTkLabel(

            bubble.body(),

            text=message,

            justify="left",

            wraplength=700,

            anchor="w",

            font=(

                "Segoe UI",

                13

            )

        )

        body.pack(

            anchor="w",

            padx=15,

            pady=(0,12)

        )

        self.messages._parent_canvas.yview_moveto(

            1.0

        )

    # ==================================================
    # AI Message
    # ==================================================

    def append_ai(

        self,

        message

    ):

        self.append_message(

            sender="WEBSTER",

            message=message

        )

    # ==================================================
    # Clear
    # ==================================================

    def clear_chat(

        self

    ):

        for widget in self.messages.winfo_children():

            widget.destroy()

    # ==================================================
    # Loading
    # ==================================================

    def set_loading(

        self,

        state=True

    ):

        if state:

            self.ring.set_state(

                "thinking"

            )

            self.title.set_subtitle(

                "Thinking..."

            )

        else:

            self.ring.set_state(

                "idle"

            )

            self.title.set_subtitle(

                "Standing By"

            )

    # ==================================================
    # Loading
    # ==================================================

    def set_loading(

        self,

        state=True

    ):

        if state:

            self.ring.set_state(

                "thinking"

            )

            self.title.set_subtitle(

                "Thinking..."

            )

        else:

            self.ring.set_state(

                "idle"

            )

            self.title.set_subtitle(

                "Standing By"

            )

    # ==================================================
    # Voice
    # ==================================================

    def toggle_voice(

        self

    ):

        self.ring.set_state(

            "listening"

        )

    # ==================================================
    # Camera
    # ==================================================

    def open_camera(

        self

    ):

        pass

    # ==================================================
    # Memory
    # ==================================================

    def open_memory(

        self

    ):

        if hasattr(

            self.controller,

            "go_memory"

        ):

            self.controller.go_memory()

    # ==================================================
    # Plugins
    # ==================================================

    def open_plugins(

        self

    ):

        if hasattr(

            self.controller,

            "go_plugins"

        ):

            self.controller.go_plugins()

    # ==================================================
    # Refresh
    # ==================================================

    def refresh(

        self

    ):

        pass

    # ==================================================
    # Resize
    # ==================================================

    def on_resize(

        self,

        event=None

    ):

        pass

