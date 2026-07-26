"""
WEBSTER AI Tools
================
Tool definitions for AI function calling.
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Tool:
    """An AI-callable tool."""
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable
    category: str = "general"


class ToolRegistry:
    """
    Registry of tools that Spidey can call.
    Maps tool names to handler functions.
    """

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def register_handler(self, name: str, description: str,
                         parameters: Dict[str, Any], handler: Callable,
                         category: str = "general"):
        tool = Tool(name=name, description=description,
                    parameters=parameters, handler=handler, category=category)
        self._tools[name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def get_all(self) -> List[Tool]:
        return list(self._tools.values())

    def get_by_category(self, category: str) -> List[Tool]:
        return [t for t in self._tools.values() if t.category == category]

    def execute(self, name: str, **kwargs) -> Any:
        tool = self.get(name)
        if not tool:
            return f"Tool '{name}' not found"
        try:
            return tool.handler(**kwargs)
        except Exception as e:
            return f"Tool '{name}' error: {e}"

    def list_tools(self) -> List[Dict[str, Any]]:
        return [{
            "name": t.name,
            "description": t.description,
            "category": t.category,
            "parameters": t.parameters,
        } for t in self._tools.values()]

    def to_openai_format(self) -> List[Dict[str, Any]]:
        """Format tools for OpenAI function calling."""
        tools = []
        for tool in self._tools.values():
            properties = {}
            required = []
            for key, param in tool.parameters.items():
                properties[key] = {
                    "type": param.get("type", "string"),
                    "description": param.get("description", ""),
                }
                if param.get("required", False):
                    required.append(key)
            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required,
                    },
                },
            })
        return tools


# Default tool definitions
def create_default_tools() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register_handler(
        name="search_web",
        description="Search the web for information",
        parameters={"query": {"type": "string", "description": "Search query", "required": True}},
        handler=lambda query: f"[Searching web for: {query}]",
        category="web",
    )

    registry.register_handler(
        name="open_app",
        description="Open a desktop application",
        parameters={"app_name": {"type": "string", "description": "Name of the app to open", "required": True}},
        handler=lambda app_name: f"[Opening app: {app_name}]",
        category="automation",
    )

    registry.register_handler(
        name="create_note",
        description="Create a new note",
        parameters={
            "title": {"type": "string", "description": "Note title", "required": True},
            "content": {"type": "string", "description": "Note content", "required": True},
        },
        handler=lambda title, content: f"[Creating note: {title}]",
        category="study",
    )

    registry.register_handler(
        name="set_reminder",
        description="Set a reminder",
        parameters={
            "message": {"type": "string", "description": "Reminder message", "required": True},
            "minutes": {"type": "number", "description": "Minutes from now", "required": True},
        },
        handler=lambda message, minutes: f"[Setting reminder: {message} in {minutes}min]",
        category="schedule",
    )

    registry.register_handler(
        name="get_time",
        description="Get the current date and time",
        parameters={},
        handler=lambda: f"[Current time: ]",
        category="utility",
    )

    registry.register_handler(
        name="calculate",
        description="Perform a calculation",
        parameters={"expression": {"type": "string", "description": "Math expression", "required": True}},
        handler=lambda expression: f"[Calculating: {expression}]",
        category="utility",
    )

    return registry
