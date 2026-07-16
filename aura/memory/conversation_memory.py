from datetime import datetime


class ConversationMemory:
    """
    Stores the conversation for the current session.

    This class does NOT save to disk.
    Saving is handled by MemoryStorage.
    """

    def __init__(self):

        self.messages = []

    # -------------------------------------------------
    # Add Messages
    # -------------------------------------------------

    def add_message(self, role, content):

        self.messages.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            }
        )

    # -------------------------------------------------

    def add_user(self, message):

        self.add_message(
            "user",
            message
        )

    # -------------------------------------------------

    def add_assistant(self, message):

        self.add_message(
            "assistant",
            message
        )

    # -------------------------------------------------
    # Get Messages
    # -------------------------------------------------

    def get_messages(self):

        return self.messages.copy()

    # -------------------------------------------------

    def get_last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]

    # -------------------------------------------------

    def get_last(self, amount=10):

        return self.messages[-amount:]

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self.messages.clear()

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export_text(self):

        output = []

        for message in self.messages:

            role = message["role"].upper()

            content = message["content"]

            output.append(
                f"{role}: {content}"
            )

        return "\n".join(output)

    # -------------------------------------------------

    def size(self):

        return len(self.messages)
