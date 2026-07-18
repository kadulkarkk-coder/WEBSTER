class AIProviderError(Exception):
    """Base AI Provider Exception"""
    pass


class InvalidAPIKey(AIProviderError):
    pass


class InvalidModel(AIProviderError):
    pass


class QuotaExceeded(AIProviderError):
    pass


class RateLimited(AIProviderError):
    pass


class NetworkError(AIProviderError):
    pass


class TimeoutError(AIProviderError):
    pass


class ServerError(AIProviderError):
    pass


class UnknownProviderError(AIProviderError):
    pass