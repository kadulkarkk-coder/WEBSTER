from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
load_dotenv(ROOT / ".env")

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

class Config:
    app_name = env("WEBSTER_NAME", "WEBSTER")
    wake_names = [x.strip().lower() for x in env("WEBSTER_WAKE_NAMES", "bindu,webster,floating orb").split(",") if x.strip()]
    provider = env("WEBSTER_AI_PROVIDER", "gemini").lower()
    model = env("WEBSTER_AI_MODEL", "gemini-2.5-flash")
    google_key = env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")
    openai_key = env("OPENAI_API_KEY")
    openrouter_key = env("OPENROUTER_API_KEY")
    fish_key = env("FISH_API_KEY")
    fish_voice = env("FISH_VOICE_ID")
    allow_camera = env("WEBSTER_ALLOW_CAMERA", "false").lower() == "true"
    data_dir = DATA
