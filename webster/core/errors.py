"""
WEBSTER Error System
====================
Hierarchical exception classes for the entire application.
"""


class WebsterError(Exception):
    """Base exception for all WEBSTER errors."""
    code = "WEBSTER_ERROR"
    message = "An unexpected error occurred."

    def __init__(self, message: str = None, details: dict = None):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class ConfigError(WebsterError):
    code = "CONFIG_ERROR"
    message = "Configuration error."


class AIError(WebsterError):
    code = "AI_ERROR"
    message = "AI provider error."


class ProviderNotFoundError(AIError):
    code = "PROVIDER_NOT_FOUND"
    message = "AI provider not found."


class ProviderNotInitializedError(AIError):
    code = "PROVIDER_NOT_INITIALIZED"
    message = "AI provider not initialized."


class APIKeyError(AIError):
    code = "API_KEY_ERROR"
    message = "API key is missing or invalid."


class QuotaExceededError(AIError):
    code = "QUOTA_EXCEEDED"
    message = "API quota exceeded."


class RateLimitError(AIError):
    code = "RATE_LIMITED"
    message = "Rate limited. Please wait."


class NetworkError(WebsterError):
    code = "NETWORK_ERROR"
    message = "Network connection error."


class MemoryError(WebsterError):
    code = "MEMORY_ERROR"
    message = "Memory system error."


class VoiceError(WebsterError):
    code = "VOICE_ERROR"
    message = "Voice system error."


class WakeWordError(VoiceError):
    code = "WAKE_WORD_ERROR"
    message = "Wake word detection error."


class STTError(VoiceError):
    code = "STT_ERROR"
    message = "Speech-to-text error."


class TTSError(VoiceError):
    code = "TTS_ERROR"
    message = "Text-to-speech error."


class PluginError(WebsterError):
    code = "PLUGIN_ERROR"
    message = "Plugin system error."


class PluginLoadError(PluginError):
    code = "PLUGIN_LOAD_ERROR"
    message = "Failed to load plugin."


class AutomationError(WebsterError):
    code = "AUTOMATION_ERROR"
    message = "Automation error."


class StudyError(WebsterError):
    code = "STUDY_ERROR"
    message = "Study hub error."


class SyncError(WebsterError):
    code = "SYNC_ERROR"
    message = "Synchronization error."


class DashboardError(WebsterError):
    code = "DASHBOARD_ERROR"
    message = "Dashboard error."


class DatabaseError(WebsterError):
    code = "DATABASE_ERROR"
    message = "Database error."
