import customtkinter as ctk

from aura.ui.widgets.glass_icon import GlassIcon


class GlassRing(

    ctk.CTkFrame

):

    """
    ==================================================

                    Glass Ring

    AI Status Indicator

    Uses:

        icons/ai/

            idle.png
            thinking.png
            listening.png
            speaking.png
            offline.png

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        state="idle",

        size=(180,180),

        **kwargs

    ):

        super().__init__(

            master,

            fg_color="transparent",

            **kwargs

        )

        self.state = state

        self.size = size

        self.build()

    # ==================================================
    # Build
    # ==================================================

    def build(

        self

    ):

        self.text = GlassIcon(

            self,

            category="ai",

            name=self.state,

            size=self.size

        )

        self.text.pack(

            expand=True,

            fill="both"

        )

    # ==================================================
    # Change State
    # ==================================================

    def set_state(

        self,

        state

    ):

        self.state = state

        self.text.set_icon(

            "ai",

            state,

            self.size

        )

    # ==================================================
    # Idle
    # ==================================================

    def idle(

        self

    ):

        self.set_state(

            "idle"

        )


    # ==================================================
    # Thinking
    # ==================================================

    def thinking(

        self

    ):

        self.set_state(

            "thinking"

        )


    # ==================================================
    # Listening
    # ==================================================

    def listening(

        self

    ):

        self.set_state(

            "listening"

        )


    # ==================================================
    # Speaking
    # ==================================================

    def speaking(

        self

    ):

        self.set_state(

            "speaking"

        )


    # ==================================================
    # Offline
    # ==================================================

    def offline(

        self

    ):

        self.set_state(

            "offline"
        )

    # ==================================================
    # Resize
    # ==================================================

    def resize(

        self,

        width,

        height

    ):

        self.size = (

            width,

            height

        )

        self.text.set_icon(

            "ai",

            self.state,

            self.size

        )

    # ==================================================
    # Get State
    # ==================================================

    def get_state(

        self

    ):

        return self.state

