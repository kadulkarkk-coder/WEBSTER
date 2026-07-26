"""
WEBSTER Event System
====================
Publish-subscribe event system for inter-module communication.
"""

import time
import uuid
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict

from webster.core.logger import Logger


@dataclass
class Event:
    """A single event in the system."""
    type: str
    data: dict = field(default_factory=dict)
    source: str = "system"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)
    priority: int = 5


class EventBus:
    """
    Central event bus for publish-subscribe communication.
    Modules can subscribe to events and publish events.
    """

    def __init__(self):
        self.logger = Logger().get_logger("EVENTS")
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._history: List[Event] = []
        self._max_history = 100

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to an event type."""
        self._subscribers[event_type].append(callback)
        self.logger.debug(f"Subscribed to '{event_type}': {callback.__name__}")

    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                cb for cb in self._subscribers[event_type] if cb != callback
            ]

    def publish(self, event_type: str, data: dict = None, source: str = "system"):
        """Publish an event to all subscribers."""
        event = Event(type=event_type, data=data or {}, source=source)
        self._history.append(event)
        self._trim_history()
        self.logger.debug(f"Event: {event_type} from {source}")
        for callback in self._subscribers.get(event_type, []):
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Event handler failed for '{event_type}': {e}")

    def publish_async(self, event_type: str, data: dict = None, source: str = "system"):
        """Publish event asynchronously."""
        import threading
        thread = threading.Thread(
            target=self.publish,
            args=(event_type, data, source),
            daemon=True
        )
        thread.start()

    def get_history(self, event_type: Optional[str] = None, limit: int = 10) -> List[Event]:
        """Get recent events."""
        if event_type:
            filtered = [e for e in self._history if e.type == event_type]
            return filtered[-limit:]
        return self._history[-limit:]

    def clear_history(self):
        self._history.clear()

    def _trim_history(self):
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

    def subscriber_count(self, event_type: str) -> int:
        return len(self._subscribers.get(event_type, []))

    def status(self) -> dict:
        return {
            "event_types": list(self._subscribers.keys()),
            "total_subscribers": sum(len(v) for v in self._subscribers.values()),
            "history_size": len(self._history),
        }
