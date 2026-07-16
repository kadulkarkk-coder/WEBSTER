from aura.memory.conversation_memory import ConversationMemory
from aura.memory.user_profile import UserProfile
from aura.memory.memory_storage import MemoryStorage


class MemoryManager:
    """
    Central manager for all AURA memory.

    Responsibilities:
        • Manage conversation memory
        • Manage user profile
        • Save everything
        • Load everything
    """

    def __init__(self):

        self.storage = MemoryStorage()

        self.conversation = ConversationMemory()

        self.profile = UserProfile()

        self.load()

    # ====================================================
    # Loading
    # ====================================================

    def load(self):

        # Load Conversation

        conversations = self.storage.load_conversations()

        self.conversation.clear()

        for message in conversations:

            role = message.get("role", "")

            content = message.get("content", "")

            if role and content:

                self.conversation.add_message(
                    role,
                    content
                )

        # Load Profile

        profile = self.storage.load_profile()

        self.profile.load(profile)

    # ====================================================
    # Saving
    # ====================================================

    def save(self):

        self.storage.save_conversations(
            self.conversation.get_messages()
        )

        self.storage.save_profile(
            self.profile.export()
        )

    # ====================================================
    # Conversation
    # ====================================================

    def add_user(self, message):

        self.conversation.add_user(message)

        self.save()

    # ----------------------------------------------------

    def add_assistant(self, message):

        self.conversation.add_assistant(message)

        self.save()

    # ----------------------------------------------------

    def get_messages(self):

        return self.conversation.get_messages()

    # ----------------------------------------------------

    def get_last_message(self):

        return self.conversation.get_last_message()

    # ----------------------------------------------------

    def clear_conversation(self):

        self.conversation.clear()

        self.save()

    # ====================================================
    # Profile
    # ====================================================

    def get_profile(self):

        return self.profile

    # ----------------------------------------------------

    def get_setting(self, key, default=None):

        return self.profile.get(key, default)

    # ----------------------------------------------------

    def set_setting(self, key, value):

        self.profile.set(
            key,
            value
        )

        self.save()

    # ====================================================
    # Utilities
    # ====================================================

    def export_chat(self):

        return self.conversation.export_text()

    # ----------------------------------------------------

    def conversation_size(self):

        return self.conversation.size()

    # ----------------------------------------------------

    def reset(self):

        self.conversation.clear()

        self.profile.reset()

        self.save()

    # ----------------------------------------------------

    def print_summary(self):

        print("=" * 40)
        print("AURA MEMORY SUMMARY")
        print("=" * 40)

        print(
            "Messages:",
            self.conversation.size()
        )

        print(
            "User:",
            self.profile.get_display_name()
        )

        print(
            "Theme:",
            self.profile.get_theme()
        )

        print("=" * 40)