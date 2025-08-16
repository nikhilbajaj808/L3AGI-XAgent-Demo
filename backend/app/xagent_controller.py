# backend/app/xagent_controller.py
from typing import List, Dict, Any, Optional
import re
from app.tool_adapter import ToolAdapter


class XAgentController:
    """
    Simple XAgent demo controller that decides which tool to call based on input text.
    """

    def __init__(self, tool_adapter: ToolAdapter) -> None:
        self.tool_adapter = tool_adapter
        self.tools = tool_adapter.get_tools()

    def run_agent(self, query: str) -> Dict[str, Any]:
        text = query.strip()
        lower = text.lower()

        # Tool selection logic
        if "echo" in lower:
            result = self.tool_adapter.invoke("echo", text=text.replace("echo", "", 1).strip())
            return self._format_response("echo", {"result": result})

        if any(k in lower for k in ("add", "sum", "+", "calculate")):
            nums = re.findall(r"-?\d+\.?\d*", text)
            if len(nums) >= 2:
                a, b = float(nums[0]), float(nums[1])
                result = self.tool_adapter.invoke("add", a=a, b=b)
                return self._format_response("add", {"a": a, "b": b, "result": result})
            else:
                return self._format_response("add", {"error": "Not enough numbers provided."})

        # Default fallback: echo
        result = self.tool_adapter.invoke("echo", text=text)
        return self._format_response("echo", {"result": result})

    def _format_response(self, tool_name: str, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Standardized response with engine and traces."""
        return {
            "engine": "xagent",
            "tool_used": tool_name,
            "observation": observation,
            "assistant": {
                "role": "assistant",
                "content": str(observation.get("result", observation))
            }
        }
