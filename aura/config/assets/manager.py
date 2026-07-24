from pathlib import Path


class Assets:

    ROOT = Path(__file__).parent

    LOGO = ROOT / "logo"

    ICONS = ROOT / "icons"

    SUITS = ROOT / "suits"

    WALLPAPERS = ROOT / "wallpapers"

    FONTS = ROOT / "fonts"

    ANIMATIONS = ROOT / "animations"

    SOUNDS = ROOT / "sounds"

    @classmethod
    def logo(

        cls,

        name

    ):

        return cls.LOGO / name

    @classmethod
    def text(

        cls,

        name

    ):

        return cls.ICONS / name

    @classmethod
    def wallpaper(

        cls,

        name

    ):

        return cls.WALLPAPERS / name

    @classmethod
    def sound(

        cls,

        name

    ):

        return cls.SOUNDS / name

    @classmethod
    def animation(

        cls,

        name

    ):

        return cls.ANIMATIONS / name