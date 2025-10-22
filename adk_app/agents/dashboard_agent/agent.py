"""Dashboard Agent - Specialized agent for database querying and analytics."""

import sys
from pathlib import Path
from google.adk.agents import Agent

# Add parent directories to path
base_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(base_dir))

from adk_app.core.settings import get_settings
from adk_app.tools.toolsets.dashboard_toolset import DashboardToolset

# Load settings
settings = get_settings()
model_config = settings.get_model_config("dashboard_agent")

# Load persona instruction
persona_path = Path(__file__).parent / "persona.md"
with open(persona_path, 'r', encoding='utf-8') as f:
    INSTRUCTION = f.read()

# Create dashboard agent
dashboard_agent = Agent(
    model=model_config.get("model_id", "gemini-2.0-flash-exp"),
    name="dashboard_agent",
    description="Specialized agent for database querying, data exploration, and analytics. Converts natural language questions into SQL queries and provides intelligent data insights.",
    instruction=INSTRUCTION,
    tools=DashboardToolset.get_tools()
)

# Export as root_agent for ADK CLI compatibility
root_agent = dashboard_agent
