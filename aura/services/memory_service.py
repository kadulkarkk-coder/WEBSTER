import json

from pathlib import Path

from aura.utils.debug import Debug


class MemoryService:
    """
    ==================================================

                AURA Memory Service V2

    ==================================================

    Handles

    • Conversation Memory
    • User Profile
    • Settings
    • Automatic Saving
    • Automatic Loading
    • Backup Support

    Future

    • Semantic Memory
    • SQLite
    • Vector Database
    • Knowledge Graph
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        root = Path(__file__).resolve().parent.parent

        self.data_folder = (
            root / "data"
        )

        self.backup_folder = (
            self.data_folder / "backups"
        )

        self.conversation_file = (
            self.data_folder / "conversation.json"
        )

        self.profile_file = (
            self.data_folder / "profile.json"
        )

        self.settings_file = (
            self.data_folder / "settings.json"
        )

        # ----------------------------------------------

        self.messages = []

        self.profile = {}

        self.settings = {}

        self.initialized = False

    # ==================================================
    # Initialize
    # ==================================================

    def initialize(self):

        Debug.log(
            "Memory",
            "Initializing Memory Service"
        )

        self._create_directories()

        self._create_files()

        self.load_all()

        self.initialized = True

        Debug.log(
            "Memory",
            "Memory Service Ready"
        )

    # ==================================================
    # Directories
    # ==================================================

    def _create_directories(self):

        self.data_folder.mkdir(

            parents=True,

            exist_ok=True

        )

        self.backup_folder.mkdir(

            parents=True,

            exist_ok=True

        )

    # ==================================================
    # Create Files
    # ==================================================

    def _create_files(self):

        self._create_json(

            self.conversation_file,

            {
                "messages": []
            }

        )

        self._create_json(

            self.profile_file,

            {

                "name": "",

                "nickname": "",

                "age": None,

                "grade": "",

                "school": "",

                "location": "",

                "interests": [],

                "skills": [],

                "goals": [],

                "facts": {}

            }

        )

        self._create_json(

            self.settings_file,

            {

                "theme": "dark",

                "provider": "dummy",

                "voice": False,

                "window": {

                    "width": 1280,

                    "height": 720

                }

            }

        )

    # ==================================================
    # Create JSON Helper
    # ==================================================

    def _create_json(

        self,

        path,

        default_data

    ):

        if path.exists():

            return

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                default_data,

                file,

                indent=4,

                ensure_ascii=False

            )

    # ==================================================
    # JSON Helpers
    # ==================================================

    def _read_json(

        self,

        path,

        default

    ):

        try:

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as file:

                return json.load(file)

        except Exception as e:

            Debug.log(

                "Memory",

                f"Read Error : {e}"

            )

            return default

    # --------------------------------------------------

    def _write_json(

        self,

        path,

        data

    ):

        try:

            with open(

                path,

                "w",

                encoding="utf-8"

            ) as file:

                json.dump(

                    data,

                    file,

                    indent=4,

                    ensure_ascii=False

                )

        except Exception as e:

            Debug.log(

                "Memory",

                f"Write Error : {e}"

            )

    # ==================================================
    # Load Everything
    # ==================================================

    def load_all(self):

        Debug.log(

            "Memory",

            "Loading Memory Files"

        )

        self.load_conversation()

        self.load_profile()

        self.load_settings()

    # ==================================================
    # Save Everything
    # ==================================================

    def save_all(self):

        Debug.log(

            "Memory",

            "Saving Memory Files"

        )

        self.save_conversation()

        self.save_profile()

        self.save_settings()
    # ==================================================
    # Conversation
    # ==================================================

    def add_user(
        self,
        message
    ):

        Debug.log(
            "Memory",
            "Saving user message"
        )

        self.messages.append({

            "role": "user",

            "content": str(message)

        })

        self.save_conversation()

    # --------------------------------------------------

    def add_assistant(
        self,
        message
    ):

        Debug.log(
            "Memory",
            "Saving assistant message"
        )

        self.messages.append({

            "role": "assistant",

            "content": str(message)

        })

        self.save_conversation()

    # --------------------------------------------------

    def add_system(
        self,
        message
    ):

        Debug.log(
            "Memory",
            "Saving system message"
        )

        self.messages.append({

            "role": "system",

            "content": str(message)

        })

        self.save_conversation()

    # ==================================================
    # Load Conversation
    # ==================================================

    def load_conversation(self):

        Debug.log(

            "Memory",

            "Loading conversation"

        )

        data = self._read_json(

            self.conversation_file,

            {

                "messages": []

            }

        )

        self.messages = data.get(

            "messages",

            []

        )

    # ==================================================
    # Save Conversation
    # ==================================================

    def save_conversation(self):

        Debug.log(

            "Memory",

            "Saving conversation"

        )

        data = {

            "messages": self.messages

        }

        self._write_json(

            self.conversation_file,

            data

        )

    # ==================================================
    # Retrieve
    # ==================================================

    def get_messages(self):

        return list(

            self.messages

        )

    # --------------------------------------------------

    def get_last_message(self):

        if not self.messages:

            return None

        return self.messages[-1]

    # --------------------------------------------------

    def get_last_messages(
        self,
        count
    ):

        return self.messages[-count:]

    # --------------------------------------------------

    def get_message(
        self,
        index
    ):

        if index < 0:

            index = len(self.messages) + index

        if index < 0:

            return None

        if index >= len(self.messages):

            return None

        return self.messages[index]

    # ==================================================
    # Statistics
    # ==================================================

    def message_count(self):

        return len(

            self.messages

        )

    # --------------------------------------------------

    def user_message_count(self):

        return sum(

            1

            for message in self.messages

            if message["role"] == "user"

        )

    # --------------------------------------------------

    def assistant_message_count(self):

        return sum(

            1

            for message in self.messages

            if message["role"] == "assistant"

        )

    # --------------------------------------------------

    def system_message_count(self):

        return sum(

            1

            for message in self.messages

            if message["role"] == "system"

        )

    # ==================================================
    # Conversation Management
    # ==================================================

    def clear_chat(self):

        Debug.log(

            "Memory",

            "Conversation cleared"

        )

        self.messages.clear()

        self.save_conversation()

    # --------------------------------------------------

    def remove_last_message(self):

        if not self.messages:

            return

        self.messages.pop()

        self.save_conversation()

    # --------------------------------------------------

    def remove_message(
        self,
        index
    ):

        if index < 0:

            index = len(self.messages) + index

        if index < 0:

            return

        if index >= len(self.messages):

            return

        del self.messages[index]

        self.save_conversation()

    # ==================================================
    # Export
    # ==================================================

    def export_chat(self):

        lines = []

        for message in self.messages:

            role = message.get(

                "role",

                "unknown"

            )

            content = message.get(

                "content",

                ""

            )

            lines.append(

                f"{role}: {content}"

            )

        return "\n".join(

            lines

        )

    # --------------------------------------------------

    def conversation_exists(self):

        return len(

            self.messages

        ) > 0
    # ==================================================
    # Profile
    # ==================================================

    def load_profile(self):

        Debug.log(

            "Memory",

            "Loading profile"

        )

        default = {

            "name": "",

            "nickname": "",

            "age": None,

            "grade": "",

            "school": "",

            "location": "",

            "occupation": "",

            "bio": "",

            "interests": [],

            "skills": [],

            "goals": [],

            "likes": [],

            "dislikes": [],

            "facts": {},

            "preferences": {}

        }

        self.profile = self._read_json(

            self.profile_file,

            default

        )

    # --------------------------------------------------

    def save_profile(self):

        Debug.log(

            "Memory",

            "Saving profile"

        )

        self._write_json(

            self.profile_file,

            self.profile

        )

    # ==================================================
    # Entire Profile
    # ==================================================

    def get_profile(self):

        return dict(

            self.profile

        )

    # --------------------------------------------------

    def set_profile(

        self,

        profile

    ):

        self.profile = dict(

            profile

        )

        self.save_profile()

    # ==================================================
    # Generic Keys
    # ==================================================

    def get_profile_value(

        self,

        key,

        default=None

    ):

        return self.profile.get(

            key,

            default

        )

    # --------------------------------------------------

    def set_profile_value(

        self,

        key,

        value

    ):

        self.profile[key] = value

        self.save_profile()

    # --------------------------------------------------

    def remove_profile_value(

        self,

        key

    ):

        if key in self.profile:

            del self.profile[key]

            self.save_profile()

    # ==================================================
    # Lists
    # ==================================================

    def add_interest(

        self,

        interest

    ):

        if interest not in self.profile["interests"]:

            self.profile["interests"].append(

                interest

            )

            self.save_profile()

    # --------------------------------------------------

    def add_skill(

        self,

        skill

    ):

        if skill not in self.profile["skills"]:

            self.profile["skills"].append(

                skill

            )

            self.save_profile()

    # --------------------------------------------------

    def add_goal(

        self,

        goal

    ):

        if goal not in self.profile["goals"]:

            self.profile["goals"].append(

                goal

            )

            self.save_profile()

    # --------------------------------------------------

    def add_like(

        self,

        item

    ):

        if item not in self.profile["likes"]:

            self.profile["likes"].append(

                item

            )

            self.save_profile()

    # --------------------------------------------------

    def add_dislike(

        self,

        item

    ):

        if item not in self.profile["dislikes"]:

            self.profile["dislikes"].append(

                item

            )

            self.save_profile()

    # ==================================================
    # Facts
    # ==================================================

    def remember(

        self,

        key,

        value

    ):

        self.profile["facts"][key] = value

        self.save_profile()

    # --------------------------------------------------

    def recall(

        self,

        key,

        default=None

    ):

        return self.profile["facts"].get(

            key,

            default

        )

    # --------------------------------------------------

    def forget(

        self,

        key

    ):

        if key in self.profile["facts"]:

            del self.profile["facts"][key]

            self.save_profile()

    # ==================================================
    # Preferences
    # ==================================================

    def set_preference(

        self,

        key,

        value

    ):

        self.profile["preferences"][key] = value

        self.save_profile()

    # --------------------------------------------------

    def get_preference(

        self,

        key,

        default=None

    ):

        return self.profile["preferences"].get(

            key,

            default

        )

    # ==================================================
    # Profile Helpers
    # ==================================================

    def profile_exists(self):

        return any(

            value

            for value in self.profile.values()

        )

    # --------------------------------------------------

    def clear_profile(self):

        self.profile.clear()

        self.load_profile()

        self.save_profile()

    # ==================================================
    # Settings
    # ==================================================

    def load_settings(self):

        Debug.log(

            "Memory",

            "Loading settings"

        )

        default = {

            "theme": "dark",

            "provider": "dummy",

            "voice": False,

            "notifications": True,

            "auto_save": True,

            "language": "English",

            "window": {

                "width": 1280,

                "height": 720,

                "maximized": False

            },

            "chat": {

                "font_size": 14,

                "auto_scroll": True,

                "show_timestamps": False

            },

            "plugins": {

                "enabled": True,

                "auto_load": True

            }

        }

        self.settings = self._read_json(

            self.settings_file,

            default

        )

    # --------------------------------------------------

    def save_settings(self):

        Debug.log(

            "Memory",

            "Saving settings"

        )

        self._write_json(

            self.settings_file,

            self.settings

        )

    # ==================================================
    # Generic Settings
    # ==================================================

    def get_setting(

        self,

        key,

        default=None

    ):

        return self.settings.get(

            key,

            default

        )

    # --------------------------------------------------

    def set_setting(

        self,

        key,

        value

    ):

        self.settings[key] = value

        self.save_settings()

    # --------------------------------------------------

    def remove_setting(

        self,

        key

    ):

        if key in self.settings:

            del self.settings[key]

            self.save_settings()

    # ==================================================
    # Window
    # ==================================================

    def get_window_size(self):

        return self.settings.get(

            "window",

            {}

        )

    # --------------------------------------------------

    def set_window_size(

        self,

        width,

        height

    ):

        self.settings["window"]["width"] = width

        self.settings["window"]["height"] = height

        self.save_settings()

    # --------------------------------------------------

    def set_window_maximized(

        self,

        value

    ):

        self.settings["window"]["maximized"] = bool(

            value

        )

        self.save_settings()

    # ==================================================
    # Theme
    # ==================================================

    def get_theme(self):

        return self.settings.get(

            "theme",

            "dark"

        )

    # --------------------------------------------------

    def set_theme(

        self,

        theme

    ):

        self.settings["theme"] = theme

        self.save_settings()

    # ==================================================
    # Provider
    # ==================================================

    def get_provider(self):

        return self.settings.get(

            "provider",

            "dummy"

        )

    # --------------------------------------------------

    def set_provider(

        self,

        provider

    ):

        self.settings["provider"] = provider

        self.save_settings()

    # ==================================================
    # Voice
    # ==================================================

    def voice_enabled(self):

        return self.settings.get(

            "voice",

            False

        )

    # --------------------------------------------------

    def enable_voice(self):

        self.settings["voice"] = True

        self.save_settings()

    # --------------------------------------------------

    def disable_voice(self):

        self.settings["voice"] = False

        self.save_settings()

    # ==================================================
    # Language
    # ==================================================

    def get_language(self):

        return self.settings.get(

            "language",

            "English"

        )

    # --------------------------------------------------

    def set_language(

        self,

        language

    ):

        self.settings["language"] = language

        self.save_settings()

    # ==================================================
    # Plugins
    # ==================================================

    def plugins_enabled(self):

        return self.settings["plugins"].get(

            "enabled",

            True

        )

    # --------------------------------------------------

    def enable_plugins(self):

        self.settings["plugins"]["enabled"] = True

        self.save_settings()

    # --------------------------------------------------

    def disable_plugins(self):

        self.settings["plugins"]["enabled"] = False

        self.save_settings()

    # ==================================================
    # Chat Preferences
    # ==================================================

    def get_chat_setting(

        self,

        key,

        default=None

    ):

        return self.settings["chat"].get(

            key,

            default

        )

    # --------------------------------------------------

    def set_chat_setting(

        self,

        key,

        value

    ):

        self.settings["chat"][key] = value

        self.save_settings()

    # ==================================================
    # Reset
    # ==================================================

    def reset_settings(self):

        self.settings.clear()

        self.load_settings()

        self.save_settings()

    # ==================================================
    # Status
    # ==================================================

    def settings_loaded(self):

        return bool(

            self.settings

        )

    # ==================================================
    # Search
    # ==================================================

    def search_messages(
        self,
        query
    ):

        query = str(query).lower()

        results = []

        for message in self.messages:

            content = message.get(
                "content",
                ""
            )

            if query in content.lower():

                results.append(
                    message
                )

        return results

    # --------------------------------------------------

    def search_profile(
        self,
        query
    ):

        query = str(query).lower()

        matches = {}

        for key, value in self.profile.items():

            if query in str(value).lower():

                matches[key] = value

        return matches

    # ==================================================
    # Statistics
    # ==================================================

    def statistics(self):

        return {

            "messages": len(
                self.messages
            ),

            "user_messages": sum(

                1

                for message in self.messages

                if message["role"] == "user"

            ),

            "assistant_messages": sum(

                1

                for message in self.messages

                if message["role"] == "assistant"

            ),

            "system_messages": sum(

                1

                for message in self.messages

                if message["role"] == "system"

            ),

            "profile_fields": len(
                self.profile
            ),

            "settings": len(
                self.settings
            )

        }

    # ==================================================
    # Backup
    # ==================================================

    def backup(self):

        Debug.log(

            "Memory",

            "Creating backup"

        )

        backup = {

            "conversation": {

                "messages": self.messages

            },

            "profile": self.profile,

            "settings": self.settings

        }

        backup_file = (

            self.backup_folder

            / "backup.json"

        )

        self._write_json(

            backup_file,

            backup

        )

    # ==================================================
    # Restore
    # ==================================================

    def restore_backup(self):

        backup_file = (

            self.backup_folder

            / "backup.json"

        )

        if not backup_file.exists():

            return False

        Debug.log(

            "Memory",

            "Restoring backup"

        )

        backup = self._read_json(

            backup_file,

            {}

        )

        conversation = backup.get(

            "conversation",

            {}

        )

        self.messages = conversation.get(

            "messages",

            []

        )

        self.profile = backup.get(

            "profile",

            {}

        )

        self.settings = backup.get(

            "settings",

            {}

        )

        self.save_all()

        return True

    # ==================================================
    # Reset
    # ==================================================

    def clear_everything(self):

        Debug.log(

            "Memory",

            "Resetting Memory"

        )

        self.messages.clear()

        self.profile.clear()

        self.settings.clear()

        self._create_files()

        self.load_all()

    # ==================================================
    # Health
    # ==================================================

    def health(self):

        return {

            "initialized": self.initialized,

            "conversation_file":

                self.conversation_file.exists(),

            "profile_file":

                self.profile_file.exists(),

            "settings_file":

                self.settings_file.exists()

        }

    # ==================================================
    # Shutdown
    # ==================================================

    def save(self):

        self.save_all()

        self.backup()

    # ==================================================
    # Status
    # ==================================================

    def get_status(self):

        return (

            "Online"

            if self.initialized

            else "Offline"

        )

    # ==================================================
    # Future Hooks
    # ==================================================

    def semantic_search(
        self,
        query
    ):

        """
        Sprint 22+

        ChromaDB

        FAISS

        SQLite Vector

        Semantic Retrieval
        """

        return []

    # --------------------------------------------------

    def sqlite_sync(self):

        """
        Sprint 23+

        SQLite Backend
        """

        pass

    # --------------------------------------------------

    def vector_sync(self):

        """
        Sprint 24+

        Vector Database
        """

        pass