"""Weather Agent - Specialized agent for weather information."""

import sys
from pathlib import Path
from google.adk.agents import Agent

# Add parent directories to path
base_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(base_dir))

from adk_app.core.settings import get_settings
from adk_app.tools.toolsets.weather_toolset import WeatherToolset

# Load settings
settings = get_settings()
model_config = settings.get_model_config("weather_agent")

# Load persona instruction
persona_path = Path(__file__).parent / "persona.md"
with open(persona_path, 'r') as f:
    INSTRUCTION = f.read()

# Create weather agent
weather_agent = Agent(
    model=model_config.get("model_id", "gemini-2.0-flash-exp"),
    name="weather_agent",
    description="Specialized agent for weather information and forecasts tailored for agriculture",
    instruction=INSTRUCTION,
    tools=WeatherToolset.get_tools()
)

# Export as root_agent for ADK CLI compatibility
root_agent = weather_agent
