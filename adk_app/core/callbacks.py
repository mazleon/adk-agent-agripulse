"""
ADK callbacks and observability hooks.
Provides logging and monitoring for agent interactions.
"""
import logging
from typing import Any, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentCallbacks:
    """Callbacks for monitoring agent behavior."""
    
    @staticmethod
    def on_agent_start(agent_name: str, query: str):
        """Called when an agent starts processing."""
        logger.info(f"[{agent_name}] Started processing query: {query[:100]}...")
    
    @staticmethod
    def on_agent_end(agent_name: str, response: str, duration: float):
        """Called when an agent finishes processing."""
        logger.info(f"[{agent_name}] Completed in {duration:.2f}s")
    
    @staticmethod
    def on_tool_call(agent_name: str, tool_name: str, args: Dict[str, Any]):
        """Called when a tool is invoked."""
        logger.info(f"[{agent_name}] Calling tool: {tool_name} with args: {args}")
    
    @staticmethod
    def on_tool_result(agent_name: str, tool_name: str, result: Any):
        """Called when a tool returns a result."""
        logger.info(f"[{agent_name}] Tool {tool_name} returned result")
    
    @staticmethod
    def on_error(agent_name: str, error: Exception):
        """Called when an error occurs."""
        logger.error(f"[{agent_name}] Error: {str(error)}", exc_info=True)
