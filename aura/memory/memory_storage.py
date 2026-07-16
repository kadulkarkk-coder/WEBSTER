import json
from pathlib import Path


class MemoryStorage:
    """
    Handles saving and loading AURA's memory files.
    """

    def __init__(self):

        self.base_path = Path("aura/data/memory")

        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.conversation_file = self.base_path / "conversations.json"

        self.profile_file = self.base_path / "profile.json"

        self._ensure_files()

    # -----------------------------------------------------
    # File Initialization
    # -----------------------------------------------------

    def _ensure_files(self):

        if not self.conversation_file.exists():

            self.save_conversations([])

        if not self.profile_file.exists():

            self.save_profile({})

    # -----------------------------------------------------
    # Conversation
    # -----------------------------------------------------

    def load_conversations(self):

        try:

            with open(
                self.conversation_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception as e:

            print("[MemoryStorage]", e)

            return []

    # -----------------------------------------------------

    def save_conversations(self, conversations):

        try:

            with open(
                self.conversation_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    conversations,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except Exception as e:

            print("[MemoryStorage]", e)

            return False

    # -----------------------------------------------------
    # Profile
    # -----------------------------------------------------

    def load_profile(self):

        try:

            with open(
                self.profile_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception as e:

            print("[MemoryStorage]", e)

            return {}

    # -----------------------------------------------------

    def save_profile(self, profile):

        try:

            with open(
                self.profile_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    profile,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except Exception as e:

            print("[MemoryStorage]", e)

            return False

    # -----------------------------------------------------
    # Utility
    # -----------------------------------------------------

    def clear_conversations(self):

        return self.save_conversations([])

    # -----------------------------------------------------

    def clear_profile(self):

        return self.save_profile({})

    # -----------------------------------------------------

    def reset(self):

        self.clear_conversations()

        self.clear_profile()
        