"""
WEBSTER UI Themes
==================
Dark glassmorphism theme with cyan + purple neon accents.
All colors are valid hex codes for CustomTkinter/Tkinter compatibility.
"""


class WebsterTheme:
    """Central theme configuration for WEBSTER UI."""

    # Core Colors
    BG_DARK = "#0a0a0f"
    BG_MID = "#12121a"
    BG_LIGHT = "#1a1a2e"
    BG_CARD = "#1e1e32"

    # Glassmorphism (solid colors since Tkinter doesn't support rgba)
    GLASS_BG = "#1a1a24"
    GLASS_BORDER = "#2a2a3a"
    GLASS_HOVER = "#252540"

    # Accent Colors
    CYAN = "#00e5ff"
    CYAN_DIM = "#005566"
    PURPLE = "#7c4dff"
    PURPLE_DIM = "#3a1a7a"
    PINK = "#ff4081"

    # Status Colors
    ONLINE = "#00e676"
    BUSY = "#ff9100"
    OFFLINE = "#ff1744"
    IDLE = "#9e9e9e"

    # Text Colors
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0c0"
    TEXT_MUTED = "#6c6c80"
    TEXT_ACCENT = "#00e5ff"

    # Sidebar
    SIDEBAR_BG = "#0e0e18"
    SIDEBAR_WIDTH = 260
    SIDEBAR_ITEM_BG = "transparent"
    SIDEBAR_ITEM_HOVER = "#1a2a3a"
    SIDEBAR_ITEM_ACTIVE = "#0a3a4a"

    # Chat
    CHAT_USER_BG = "#0a2a3a"
    CHAT_AI_BG = "#1a0a3a"
    CHAT_BORDER_RADIUS = 16

    # Dimensions
    BORDER_RADIUS_SM = 8
    BORDER_RADIUS_MD = 12
    BORDER_RADIUS_LG = 16
    BORDER_RADIUS_XL = 24

    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SM = 11
    FONT_SIZE_MD = 13
    FONT_SIZE_LG = 16
    FONT_SIZE_XL = 20
    FONT_SIZE_XXL = 28

    # Animation
    ANIMATION_FAST = 100
    ANIMATION_NORMAL = 200
    ANIMATION_SLOW = 400

    @classmethod
    def as_dict(cls) -> dict:
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("_") and not callable(v)}

    @classmethod
    def gradient(cls, color1: str, color2: str) -> tuple:
        return (color1, color2)

    @classmethod
    def accent_gradient(cls) -> tuple:
        return (cls.CYAN, cls.PURPLE)
