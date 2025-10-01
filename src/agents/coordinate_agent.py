"""
Coordinate Agent - Main routing agent for AgriPulse AI.
Classifies user queries and routes them to appropriate specialized agents.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Add parent directory to path for imports
agent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(agent_dir))

from weather_agent.agent import root_agent as weather_agent

# Load environment variables
load_dotenv()
os.environ.setdefault('GOOGLE_API_KEY', os.getenv('GOOGLE_API_KEY', ''))

INSTRUCTION = """
You are the Coordinate Agent for AgriPulse AI, an intelligent agricultural assistant system.

Your primary role is to understand user queries and route them to the appropriate specialized agent:

1. **Weather Agent** - Handles all weather-related queries including:
   - Current weather conditions for any location
   - Weather forecasts for specific dates
   - Temperature, precipitation, humidity, wind information
   - Agricultural weather insights

2. **Yield Prediction Agent** (Coming soon) - Will handle:
   - Crop yield predictions
   - Agricultural planning
   - Harvest forecasting

**How to operate:**
- Analyze the user's question carefully
- If the query is about weather, climate, temperature, rain, forecast, or atmospheric conditions, use the 'weather_agent' tool
- Provide the user's query directly to the specialized agent
- Present the specialized agent's response in a professional, clear manner
- If a query doesn't fit any specialized agent, provide general agricultural assistance

**Response Guidelines:**
- Be professional and farmer-friendly
- Always acknowledge what you're doing (e.g., "Let me check the weather for you...")
- Format responses clearly with proper sections
- If you're unsure about a query, ask for clarification

**Examples:**
- "What's the weather in London?" → Route to weather_agent
- "Will it rain tomorrow in Paris?" → Route to weather_agent
- "Weather forecast for next week in Tokyo" → Route to weather_agent
- "Hello" or "Hi" → Greet and explain your capabilities
"""

# Wrap weather agent as a tool
weather_tool = AgentTool(agent=weather_agent)

# Create the coordinate agent
root_agent = Agent(
    name="coordinate_agent",
    description="Main coordinator agent for AgriPulse AI - routes queries to specialized agents",
    instruction=INSTRUCTION,
    tools=[weather_tool],
    model="gemini-2.0-flash-exp",
)