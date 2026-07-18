from copy import deepcopy


class UserProfile:
    """
    Stores user preferences for AURA.

    This class only manages the profile in memory.
    Loading and saving are handled by MemoryStorage.
    """

    DEFAULT_PROFILE = {

        "display_name": "User",

        "theme": "dark",

        "accent_color": "black",

        "language": "en",

        "voice_enabled": False,

        "wake_word": "Hey AURA",

        "widget_enabled": False,

        "widget_position": "bottom_right",

        "start_with_windows": False,

        "tts_enabled": False,

        "stt_enabled": False,

        "preferred_ai": "local",

        "study_mode": True,

        "plugins_enabled": True,

        "vision_enabled": False,

        "gesture_enabled": False,

        "notifications": True
    }

    def __init__(self):

        self.profile = deepcopy(self.DEFAULT_PROFILE)

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load(self, data):

        if not isinstance(data, dict):
            return

        self.profile.update(data)

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(self):

        return deepcopy(self.profile)

    # -------------------------------------------------
    # Generic
    # -------------------------------------------------

    def get(self, key, default=None):

        return self.profile.get(key, default)

    def set(self, key, value):

        self.profile[key] = value

    def has(self, key):

        return key in self.profile

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(self):

        self.profile = deepcopy(self.DEFAULT_PROFILE)

    # -------------------------------------------------
    # Convenience Helpers
    # -------------------------------------------------

    def get_display_name(self):

        return self.get("display_name")

    def set_display_name(self, name):

        self.set("display_name", name)

    # ----------------------------

    def get_theme(self):

        return self.get("theme")

    def set_theme(self, theme):

        self.set("theme", theme)

    # ----------------------------

    def enable_voice(self):

        self.set("voice_enabled", True)

    def disable_voice(self):

        self.set("voice_enabled", False)

    # ----------------------------

    def enable_widget(self):

        self.set("widget_enabled", True)

    def disable_widget(self):

        self.set("widget_enabled", False)

    # ----------------------------

    def enable_gestures(self):

        self.set("gesture_enabled", True)

    def disable_gestures(self):

        self.set("gesture_enabled", False)

    # ----------------------------

    def enable_plugins(self):

        self.set("plugins_enabled", True)

    def disable_plugins(self):

        self.set("plugins_enabled", False)
