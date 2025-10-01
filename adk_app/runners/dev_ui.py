"""
Development UI runner for AgriPulse AI agents.
Provides an interactive interface for testing agents.
"""
import asyncio
import logging
from google.adk.runners import Runner
from adk_app.core.settings import get_settings
from adk_app.core.memory import get_memory_manager
from adk_app.agents.multi.coordinator import coordinator_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_dev_ui():
    """Run the development UI for the coordinator agent."""
    settings = get_settings()
    
    logger.info("🌾 Starting AgriPulse AI Development UI...")
    logger.info(f"Port: {settings.dev_ui_port}")
    
    # Get session service
    memory_manager = get_memory_manager()
    session_service = memory_manager.get_session_service()
    
    # Create runner
    runner = Runner(
        agent=coordinator_agent,
        app_name="agripulse",
        session_service=session_service
    )
    
    logger.info("✅ AgriPulse AI is ready!")
    logger.info("Available agents: weather_agent, yield_agent, coordinator_agent")
    
    # Note: The actual ADK dev UI would be launched here
    # For now, this is a placeholder for the runner setup
    
    return runner


def main():
    """Main entry point for dev UI."""
    asyncio.run(run_dev_ui())


if __name__ == "__main__":
    main()
