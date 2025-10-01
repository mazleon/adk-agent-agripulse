"""Yield Prediction Agent - Specialized agent for crop yield forecasting."""

import sys
from pathlib import Path
from google.adk.agents import Agent

# Add parent directories to path
base_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(base_dir))

from adk_app.core.settings import get_settings
from adk_app.tools.toolsets.yield_toolset import YieldToolset

# Load settings
settings = get_settings()
model_config = settings.get_model_config("yield_agent")

# Load persona instruction
persona_path = Path(__file__).parent / "persona.md"
with open(persona_path, 'r') as f:
    INSTRUCTION = f.read()

# Create yield prediction agent
yield_agent = Agent(
    model=model_config.get("model_id", "gemini-2.0-flash-exp"),
    name="yield_agent",
    description="Specialized agent for crop yield prediction and agricultural planning",
    instruction=INSTRUCTION,
    tools=YieldToolset.get_tools()
)

# Export as root_agent for ADK CLI compatibility
root_agent = yield_agent
