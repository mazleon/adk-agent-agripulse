"""In-memory session storage for development."""

from google.adk.sessions import InMemorySessionService


def get_session_service():
    """Get in-memory session service for development."""
    return InMemorySessionService()
