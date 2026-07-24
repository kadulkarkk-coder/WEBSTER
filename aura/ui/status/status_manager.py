from aura.utils.debug import Debug


class StatusManager:
    """
    Central Status Manager

    Responsible for:

    • Current AURA state
    • Orb state
    • UI text
    • Future voice status
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        self.states = {

            "idle": {

                "image": "idle",

                "text": "Ready"

            },

            "thinking": {

                "image": "thinking",

                "text": "WEBSTER is thinking..."

            },

            "listening": {

                "image": "listening",

                "text": "Listening..."

            },

            "speaking": {

                "image": "speaking",

                "text": "Speaking..."

            },

            "offline": {

                "image": "offline",

                "text": "Offline"

            },

            "sleeping": {

                "emoji": "🌙",

                "text": "Sleeping..."

            },

            "vision": {

                "emoji": "📷",

                "text": "Scanning..."

            },

            "searching": {

                "emoji": "🔎",

                "text": "Searching..."

            },

            "coding": {

                "emoji": "💻",

                "text": "Coding..."

            },

            "error": {

                "emoji": "error",

                "text": "An error occurred."

            }

        }

        self.current_state = "idle"

        self.listeners = []

    # ==================================================
    # State
    # ==================================================

    def set_state(

        self,

        state

    ):

        if state not in self.states:

            Debug.log(

                "Status",

                f"Unknown state '{state}'"

            )

            return

        Debug.log(

            "Status",

            f"Changing state -> {state}"

        )

        self.current_state = state

        self.notify_listeners()

    # ==================================================
    # Listeners
    # ==================================================

    def register_listener(

        self,

        listener

    ):

        if listener not in self.listeners:

            self.listeners.append(

                listener

            )

    # --------------------------------------------------

    def unregister_listener(

        self,

        listener

    ):

        if listener in self.listeners:

            self.listeners.remove(

                listener

            )

    # --------------------------------------------------

    def notify_listeners(

        self

    ):

        for listener in self.listeners:

            try:

                listener(

                    self.current_state

                )

            except Exception as e:

                Debug.log(

                    "Status",

                    str(e)

                )

    # --------------------------------------------------

    # ==================================================
    # Status Object
    # ==================================================

    def get_status(self):

        return self.states[
        self.current_state
    ]

    # --------------------------------------------------

    def get_text(self):

        return self.states[
            self.current_state
        ]["text"]

    # --------------------------------------------------

    def get_image(

        self

    ):

        return self.states[
            self.current_state
        ]["image"]

    # ==================================================
    # Convenience Methods
    # ==================================================

    def idle(self):

        self.set_state("idle")

    # --------------------------------------------------

    def thinking(self):

        self.set_state("thinking")

    # --------------------------------------------------

    def listening(self):

        self.set_state("listening")

    # --------------------------------------------------

    def offline(self):

        self.set_state(

            "offline"

        )

    # --------------------------------------------------

    def sleeping(self):

        self.set_state(

            "sleeping"

        )

    # --------------------------------------------------

    def vision(self):

        self.set_state(

            "vision"

        )

    # --------------------------------------------------

    def searching(self):

        self.set_state(

            "searching"

        )

    # --------------------------------------------------

    def coding(self):

        self.set_state(

            "coding"

        )
    
    # --------------------------------------------------

    def speaking(self):

        self.set_state("speaking")

    # --------------------------------------------------

    def error(self):

        self.set_state("error")

    # ==================================================
    # Helpers
    # ==================================================

    def is_idle(self):

        return self.current_state == "idle"

    # --------------------------------------------------

    def is_thinking(self):

        return self.current_state == "thinking"

    # --------------------------------------------------

    def is_listening(self):

        return self.current_state == "listening"

    
    # --------------------------------------------------

    def is_offline(self):

        return self.current_state == "offline"

    # --------------------------------------------------

    def is_sleeping(self):

        return self.current_state == "sleeping"

    # --------------------------------------------------

    def is_vision(self):

        return self.current_state == "vision"

    # --------------------------------------------------

    def is_searching(self):

        return self.current_state == "searching"

    # --------------------------------------------------

    def is_coding(self):

        return self.current_state == "coding"
    
    # --------------------------------------------------

    def is_speaking(self):

        return self.current_state == "speaking"

    # --------------------------------------------------

    def is_error(self):

        return self.current_state == "error"