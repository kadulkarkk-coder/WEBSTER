from PIL import Image

import customtkinter as ctk

from aura.config.i_assets import Assets


class AssetLoader:

    _cache = {}

    # ==================================================
    # Generic Loader
    # ==================================================

    @classmethod
    def load(

        cls,

        path,

        size=None

    ):

        key = (

            str(path),

            size

        )

        if key in cls._cache:

            return cls._cache[key]

        print(f"Loading asset: {path}")
        
        image = Image.open(

            path

        )

        if size is None:

            size = image.size

        ctk_image = ctk.CTkImage(

            light_image=image,

            dark_image=image,

            size=size

        )

        cls._cache[key] = ctk_image

        return ctk_image

    # ==================================================
    # Panels
    # ==================================================

    @classmethod
    def panel(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.panel(name),

            size

        )

    # ==================================================
    # Buttons
    # ==================================================

    @classmethod
    def button(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.button(name),

            size

        )

    # ==================================================
    # Icons
    # ==================================================

    @classmethod
    def text(

        cls,

        category,

        name,

        size=None

    ):

        return cls.load(

            Assets.text(

                category,

                name

            ),

            size

        )

    # ==================================================
    # Bars
    # ==================================================

    @classmethod
    def bar(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.bar(name),

            size

        )

    # ==================================================
    # Frames
    # ==================================================

    @classmethod
    def frame(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.frame(name),

            size

        )

    # ==================================================
    # Decorations
    # ==================================================

    @classmethod
    def decoration(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.decoration(name),

            size

        )

    # ==================================================
    # Widgets
    # ==================================================

    @classmethod
    def widget(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.widget(name),

            size

        )

    # ==================================================
    # Wallpapers
    # ==================================================

    @classmethod
    def wallpaper(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.wallpaper(name),

            size

        )

    # ==================================================
    # Clear Cache
    # ==================================================

    @classmethod
    def clear_cache(

        cls

    ):

        cls._cache.clear()

    # ==================================================
    # Rings
    # ==================================================

    @classmethod
    def ring(

        cls,

        state,

        size=None

    ):

        return cls.load(

            Assets.ring(

                state

            ) / "ring.png",

            size

        )

    # ==================================================
    # Cards
    # ==================================================

    @classmethod
    def card(

        cls,

        name,

        size=None

    ):

        return cls.load(

            Assets.card(

                name

            ),

            size

        )