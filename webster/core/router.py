"""
WEBSTER Request Router
======================
Intelligently routes requests to the appropriate subsystem.
"""

from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum, auto
import re

from webster.core.logger import Logger


class RouteTarget(Enum):
    """Available routing targets."""
    AI = "ai"
    STUDY = "study"
    AUTOMATION = "automation"
    VOICE = "voice"
    MEMORY = "memory"
    PLUGIN = "plugin"
    SYSTEM = "system"
    DASHBOARD = "dashboard"
    SEARCH = "search"
    HELP = "help"


@dataclass
class Route:
    """A route mapping intent to handler."""
    pattern: str
    target: RouteTarget
    handler: Optional[Callable] = None
    priority: int = 5
    keywords: List[str] = field(default_factory=list)


@dataclass
class RoutingResult:
    """Result of routing a request."""
    target: RouteTarget
    confidence: float
    handler: Optional[Callable] = None
    params: dict = field(default_factory=dict)
    original_input: str = ""


class RequestRouter:
    """
    Routes user requests to the correct subsystem.
    
    Uses pattern matching and keyword analysis to determine
    which part of WEBSTER should handle each request.
    """

    def __init__(self):
        self.logger = Logger().get_logger("ROUTER")
        self._routes: List[Route] = []
        self._register_default_routes()
        self.logger.info("Request router initialized")

    def _register_default_routes(self):
        """Register built-in routes."""
        # Study routes
        self.register_route(Route(
            pattern=r"(study|learn|flashcard|quiz|note|pdf|subject|exam)",
            target=RouteTarget.STUDY,
            priority=8,
            keywords=["study", "learn", "flashcard", "quiz", "note", "pdf", "exam", "subject"]
        ))

        # Automation routes
        self.register_route(Route(
            pattern=r"(open|launch|close|start|stop|run|execute|file|app|browser|search)",
            target=RouteTarget.AUTOMATION,
            priority=7,
            keywords=["open", "launch", "close", "start", "stop", "run", "execute"]
        ))

        # Voice routes
        self.register_route(Route(
            pattern=r"(speak|say|read|listen|voice|pronounce)",
            target=RouteTarget.VOICE,
            priority=6,
            keywords=["speak", "say", "read aloud", "voice", "pronounce"]
        ))

        # Memory routes
        self.register_route(Route(
            pattern=r"(remember|forget|recall|memory|remind|save)",
            target=RouteTarget.MEMORY,
            priority=6,
            keywords=["remember", "forget", "recall", "memory", "remind"]
        ))

        # Help route
        self.register_route(Route(
            pattern=r"(help|what can you|capabilities|commands)",
            target=RouteTarget.HELP,
            priority=10,
            keywords=["help", "capabilities", "commands", "what can you do"]
        ))

        # Default AI route (lowest priority - catches everything else)
        self.register_route(Route(
            pattern=r".*",
            target=RouteTarget.AI,
            priority=1,
            keywords=[]
        ))

    def register_route(self, route: Route):
        """Register a new route."""
        self._routes.append(route)
        self._routes.sort(key=lambda r: r.priority, reverse=True)

    def register_handler(self, target: RouteTarget, handler: Callable):
        """Register a handler for a route target."""
        for route in self._routes:
            if route.target == target:
                route.handler = handler
                break

    def route(self, input_text: str) -> RoutingResult:
        """Route input to the best matching target."""
        input_lower = input_text.lower()
        
        for route in self._routes:
            # Check pattern match
            if re.search(route.pattern, input_lower, re.IGNORECASE):
                # Calculate confidence
                confidence = self._calculate_confidence(input_lower, route)
                
                # Extract parameters
                params = self._extract_params(input_text, route.target)
                
                self.logger.debug(f"Routed to {route.target.value} (confidence: {confidence:.2f})")
                
                return RoutingResult(
                    target=route.target,
                    confidence=confidence,
                    handler=route.handler,
                    params=params,
                    original_input=input_text
                )

        # Fallback to AI
        return RoutingResult(
            target=RouteTarget.AI,
            confidence=0.5,
            original_input=input_text
        )

    def _calculate_confidence(self, input_lower: str, route: Route) -> float:
        """Calculate confidence score for a route match."""
        if not route.keywords:
            return 0.3
        
        matched_keywords = sum(1 for kw in route.keywords if kw in input_lower)
        base = min(matched_keywords / max(len(route.keywords), 1) * 2, 1.0)
        priority_bonus = route.priority / 10 * 0.2
        
        return min(base + priority_bonus, 1.0)

    def _extract_params(self, input_text: str, target: RouteTarget) -> dict:
        """Extract parameters from input based on target."""
        params = {"original": input_text}
        
        if target == RouteTarget.STUDY:
            # Extract subject/topic
            for prefix in ["about", "on", "for", "of"]:
                if f" {prefix} " in input_text.lower():
                    params["topic"] = input_text.lower().split(f" {prefix} ")[-1].strip()
                    break
        
        elif target == RouteTarget.AUTOMATION:
            # Extract action and target
            actions = ["open", "launch", "close", "start", "stop", "run"]
            for action in actions:
                if input_text.lower().startswith(action):
                    params["action"] = action
                    params["target"] = input_text[len(action):].strip()
                    break
        
        elif target == RouteTarget.MEMORY:
            # Extract what to remember
            for prefix in ["remember", "save", "store"]:
                if input_text.lower().startswith(prefix):
                    params["content"] = input_text[len(prefix):].strip()
                    break
        
        return params

    def route_batch(self, inputs: List[str]) -> List[RoutingResult]:
        """Route multiple inputs at once."""
        return [self.route(inp) for inp in inputs]

    def get_available_targets(self) -> List[str]:
        """Get list of all available routing targets."""
        return [t.value for t in RouteTarget]

    def get_routes(self) -> List[dict]:
        """Get all registered routes as dicts."""
        return [
            {
                "target": r.target.value,
                "pattern": r.pattern,
                "priority": r.priority,
                "keywords": r.keywords
            }
            for r in self._routes
        ]

    def clear_routes(self):
        """Clear all routes and re-register defaults."""
        self._routes.clear()
        self._register_default_routes()
