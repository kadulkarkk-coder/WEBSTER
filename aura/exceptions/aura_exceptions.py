class AuraError(Exception):
    """Base exception for AURA."""
    pass


class ConfigurationError(AuraError):
    """Raised when configuration cannot be loaded."""
    pass


class LoggerError(AuraError):
    """Raised when logging fails."""
    pass