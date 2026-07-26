"""
WEBSTER Branding Constants
===========================
All brand names, version info, and display constants in one place.
"""

# Application
APP_NAME = "WEBSTER"
APP_NAME_LONG = "Workspace for Enhanced Business, Study, Technology, Engineering & Research"
VERSION = "0.1.0"
VERSION_DISPLAY = f"v{VERSION}"
COPYRIGHT = "2026 WEBSTER Ecosystem"

# AI Companion
AI_NAME = "Spidey"
AI_NAME_LONG = "Smartest Pal In Doing Everything Your-way"
AI_TAGLINE = "Your intelligent digital companion"
WAKE_WORD = "hey spidey"

# Intelligence Engine
ENGINE_NAME = "HELVAC"
ENGINE_NAME_LONG = "Hyper-Enhanced Learning, Vision & Autonomous Core"
ENGINE_TAGLINE = "Modular intelligence coordination engine"

# UI Constants
WINDOW_TITLE = f"{APP_NAME} - {AI_NAME}"
WINDOW_MIN_WIDTH = 1280
WINDOW_MIN_HEIGHT = 720
WINDOW_DEFAULT_WIDTH = 1600
WINDOW_DEFAULT_HEIGHT = 900
SIDEBAR_WIDTH = 285

# Theme
DEFAULT_THEME = "dark"
ACCENT_COLOR_PRIMARY = "#00D4FF"
ACCENT_COLOR_SECONDARY = "#A855F7"
ACCENT_COLOR_TERTIARY = "#06B6D4"
BACKGROUND_DARK = "#0A0A0F"
BACKGROUND_LIGHT = "#FFFFFF"
SURFACE_DARK = "#12121A"
SURFACE_LIGHT = "#F5F5F5"
GLASS_BG = "rgba(18, 18, 26, 0.85)"
GLASS_BORDER = "rgba(255, 255, 255, 0.08)"

# AI Providers
AVAILABLE_PROVIDERS = {
    "gemini": "Google Gemini",
    "openai": "OpenAI GPT",
    "ollama": "Ollama (Local)",
}
DEFAULT_PROVIDER = "gemini"

# Paths
DATA_DIR = "data"
MEMORY_DIR = "data/memory"
LOGS_DIR = "logs"
DATABASE_DIR = "database"
VECTOR_STORE_DIR = "database/vector_store"
PLUGINS_DIR = "plugins"
ASSETS_DIR = "assets"

# Features
FEATURES = {
    "chat": True,
    "voice": True,
    "study": True,
    "automation": True,
    "dashboard": True,
    "plugins": True,
    "widgets": True,
    "mobile": False,
    "sync": False,
}
