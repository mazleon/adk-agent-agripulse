"""
Session memory adapters for ADK.
Provides in-memory and persistent storage options.
"""
from google.adk.sessions import InMemorySessionService
from typing import Optional


class MemoryManager:
    """Manages session memory services."""
    
    def __init__(self, service_type: str = "in_memory"):
        self.service_type = service_type
        self._service = None
    
    def get_session_service(self):
        """Get the appropriate session service."""
        if self._service is None:
            if self.service_type == "in_memory":
                self._service = InMemorySessionService()
            # Add other service types here (Redis, etc.)
            else:
                self._service = InMemorySessionService()
        return self._service


# Global memory manager instance
_memory_manager: Optional[MemoryManager] = None


def get_memory_manager(service_type: str = "in_memory") -> MemoryManager:
    """Get or create the global memory manager."""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager(service_type)
    return _memory_manager
