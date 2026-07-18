class OrbController:
    """
    Controls every visual state of AURA's Orb.

    ChatPage never changes colors,
    emojis or status directly.

    It only calls:

        orb.set_state("thinking")
    """

    STATES = {

        "idle": {
            "emoji": "🔵",
            "text": "How can I help you today?"
        },

        "listening": {
            "emoji": "🟢",
            "text": "Listening..."
        },

        "thinking": {
            "emoji": "🟣",
            "text": "WEBSTER is thinking..."
        },

        "speaking": {
            "emoji": "🟡",
            "text": "Speaking..."
        },

        "error": {
            "emoji": "🔴",
            "text": "Something went wrong."
        }

    }

    # -----------------------------------------

    def __init__(self, orb_label, status_label):

        self.orb = orb_label

        self.status = status_label

        self.current_state = None

        self.set_state("idle")

    # -----------------------------------------

    def set_state(self, state):

        if state not in self.STATES:

            state = "error"

        config = self.STATES[state]

        self.orb.configure(
            text=config["emoji"]
        )

        self.status.configure(
            text=config["text"]
        )

        self.current_state = state

    # -----------------------------------------

    def idle(self):

        self.set_state("idle")

    # -----------------------------------------

    def listening(self):

        self.set_state("listening")

    # -----------------------------------------

    def thinking(self):

        self.set_state("thinking")

    # -----------------------------------------

    def speaking(self):

        self.set_state("speaking")

    # -----------------------------------------

    def error(self):

        self.set_state("error")

    # -----------------------------------------

    def get_state(self):

        return self.current_state