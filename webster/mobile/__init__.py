"""WEBSTER Mobile Companion - Web-based mobile interface."""

def get_mobile_server(*args, **kwargs):
    """Lazy import to avoid FastAPI/uvicorn loading issues."""
    from webster.mobile.server import MobileServer
    return MobileServer(*args, **kwargs)
