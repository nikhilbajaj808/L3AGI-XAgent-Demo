# backend/app/tool_adapter.py
from typing import List, Dict, Any, Callable


class ToolAdapter:
    """
    Central registry for tools.
    Each tool has a name, description, and an execution function.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register demo tools here."""
        self.register(
            name="echo",
            description="Echo back the given text.",
            func=lambda text: text
        )
        self.register(
            name="add",
            description="Add two numbers provided in a dict {'a': num1, 'b': num2}.",
            func=lambda a, b: a + b
        )

    def register(self, name: str, description: str, func: Callable):
        self._tools[name] = {
            "name": name,
            "description": description,
            "func": func
        }

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return metadata for all registered tools."""
        return [
            {"name": v["name"], "description": v["description"]}
            for v in self._tools.values()
        ]

    def invoke(self, name: str, **kwargs) -> Any:
        """Call a registered tool by name with keyword args."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found.")
        return self._tools[name]["func"](**kwargs)
