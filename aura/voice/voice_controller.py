class VoiceController:

    def __init__(self):

        self.enabled = False
        self.listening = False
        self.speaking = False

    # ==================================================
    # Enable / Disable
    # ==================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

        self.listening = False
        self.speaking = False

    # ==================================================
    # Listening
    # ==================================================

    def start_listening(self):

        if not self.enabled:
            return False

        self.listening = True

        return True

    def stop_listening(self):

        self.listening = False

    # ==================================================
    # Speaking
    # ==================================================

    def start_speaking(self):

        if not self.enabled:
            return False

        self.speaking = True

        return True

    def stop_speaking(self):

        self.speaking = False

    # ==================================================
    # Status
    # ==================================================

    def is_enabled(self):

        return self.enabled

    def is_listening(self):

        return self.listening

    def is_speaking(self):

        return self.speaking

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):

        self.listening = False
        self.speaking = False