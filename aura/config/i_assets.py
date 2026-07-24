from pathlib import Path


class Assets:

    # ==================================================
    # Root Asset Folder
    # ==================================================

    ROOT = Path(__file__).resolve().parent.parent / "config/assets"

    # ==================================================
    # Current Theme
    # ==================================================

    CURRENT_THEME = "brand_new_day"

    # ==================================================
    # Theme Folder
    # ==================================================

    THEME = ROOT / "themes" / CURRENT_THEME

    # ==================================================
    # Theme Sections
    # ==================================================

    PANELS = THEME / "panels"

    BUTTONS = THEME / "buttons"

    BARS = THEME / "bars"

    CARDS = THEME / "cards"

    FRAMES = THEME / "frames"

    DECORATIONS = THEME / "decorations"

    ICONS = THEME / "icons"

    RINGS = THEME / "rings"

    WIDGETS = THEME / "widgets"

    WALLPAPERS = THEME / "wallpapers"

    CURSORS = THEME / "cursors"

    # ==================================================
    # Global Assets
    # ==================================================

    FONTS = ROOT / "fonts"

    AUDIO = ROOT / "audio"

    VIDEOS = ROOT / "videos"

    ANIMATIONS = ROOT / "animations"

    TEMP = ROOT / "temp"

    # ==================================================
    # Helper
    # ==================================================

    @staticmethod
    def panel(name):

        return Assets.PANELS / f"{name}.png"

    @staticmethod
    def button(name):

        return Assets.BUTTONS / f"{name}.png"

    @staticmethod
    def bar(name):

        return Assets.BARS / f"{name}.png"

    @staticmethod
    def card(name):

        return Assets.CARDS / f"{name}.png"

    @staticmethod
    def frame(name):

        return Assets.FRAMES / f"{name}.png"

    @staticmethod
    def decoration(name):

        return Assets.DECORATIONS / f"{name}.png"

    @staticmethod
    def text(category, name):

        return Assets.ICONS / category / f"{name}.png"

    @staticmethod
    def ring(

        state

    ):

        return Assets.RINGS / state
    
    @staticmethod
    def widget(name):

        return Assets.WIDGETS / f"{name}.png"

    @staticmethod
    def wallpaper(name):

        return Assets.WALLPAPERS / f"{name}.png"

    @staticmethod
    def cursor(name):

        return Assets.CURSORS / f"{name}.cur"

    # ==================================================
    # Theme Switching
    # ==================================================

    @classmethod
    def set_theme(cls, theme_name):

        cls.CURRENT_THEME = theme_name

        cls.THEME = cls.ROOT / "themes" / theme_name

        cls.PANELS = cls.THEME / "panels"

        cls.BUTTONS = cls.THEME / "buttons"

        cls.BARS = cls.THEME / "bars"

        cls.CARDS = cls.THEME / "cards"

        cls.FRAMES = cls.THEME / "frames"

        cls.DECORATIONS = cls.THEME / "decorations"

        cls.ICONS = cls.THEME / "icons"

        cls.RINGS = cls.THEME / "rings"

        cls.WIDGETS = cls.THEME / "widgets"

        cls.WALLPAPERS = cls.THEME / "wallpapers"

        cls.CURSORS = cls.THEME / "cursors"