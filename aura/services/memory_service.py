from aura.memory.memory_manager import MemoryManager


class MemoryService:

    def __init__(self):

        self.manager = MemoryManager()

        self.initialized = False

    # ==================================================
    # Service Life Cycle
    # ==================================================

    def initialize(self):

        self.initialized = True

        print("[Memory] Service Initialized")

    # --------------------------------------------------

    def shutdown(self):

        self.manager.save()

        self.initialized = False

        print("[Memory] Service Stopped")

    # --------------------------------------------------

    def get_status(self):

        if self.initialized:
            return "Running"

        return "Stopped"

    # ==================================================
    # Conversation
    # ==================================================

    def add_user(self, message):

        self.manager.add_user(message)

    # --------------------------------------------------

    def add_assistant(self, message):

        self.manager.add_assistant(message)

    # --------------------------------------------------

    def get_messages(self):

        return self.manager.get_messages()

    # --------------------------------------------------

    def clear_chat(self):

        self.manager.clear_conversation()

    # --------------------------------------------------

    def export_chat(self):

        return self.manager.export_chat()

    # ==================================================
    # Profile
    # ==================================================

    def get_profile(self):

        return self.manager.get_profile()

    # --------------------------------------------------

    def get_setting(self, key, default=None):

        return self.manager.get_setting(key, default)

    # --------------------------------------------------

    def set_setting(self, key, value):

        self.manager.set_setting(key, value)

    # ==================================================
    # Utility
    # ==================================================

    def reset(self):

        self.manager.reset()

    # --------------------------------------------------

    def save(self):

        self.manager.save()

    # --------------------------------------------------

    def load(self):

        self.manager.load()

    # --------------------------------------------------

    def get_manager(self):

        return self.manager