"""WEBSTER Dashboard - FastAPI web dashboard."""

def get_dashboard_server(*args, **kwargs):
    """Lazy import to avoid FastAPI/uvicorn loading issues."""
    from webster.dashboard.server import DashboardServer
    return DashboardServer(*args, **kwargs)
