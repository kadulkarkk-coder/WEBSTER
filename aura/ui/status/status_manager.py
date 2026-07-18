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

                "emoji": "🔵",

                "text": "Ready"

            },

            "thinking": {

                "emoji": "🟣",

                "text": "WEBSTER is thinking..."

            },

            "listening": {

                "emoji": "🟢",

                "text": "Listening..."

            },

            "speaking": {

                "emoji": "🟡",

                "text": "Speaking..."

            },

            "error": {

                "emoji": "🔴",

                "text": "An error occurred."

            }

        }

        self.current_state = "idle"

    # ==================================================
    # State
    # ==================================================

    def set_state(self, state):

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

    def get_emoji(self):

        return self.states[
            self.current_state
        ]["emoji"]

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

    def is_speaking(self):

        return self.current_state == "speaking"

    # --------------------------------------------------

    def is_error(self):

        return self.current_state == "error"