"""Weather Agent - Specialized agent for handling weather-related queries.
Provides current weather information and forecasts for specific locations.
"""
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import sys
from pathlib import Path

# Add parent directory to path for imports
agent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(agent_dir))

from tools.weather_tool import get_weather_report

# Load API key from environment
load_dotenv()
os.environ.setdefault('GOOGLE_API_KEY', os.getenv('GOOGLE_API_KEY', ''))

INSTRUCTION = """
You are a specialized Weather Agent for AgriPulse AI.

Your responsibilities:
1. Answer weather-related questions for specific locations
2. Provide current weather conditions including temperature, humidity, wind speed, and precipitation
3. Offer weather forecasts when users ask about future dates
4. Present weather information in a clear, professional, and farmer-friendly manner

Guidelines:
- Always use the 'get_weather_report' tool to fetch accurate weather data
- If the tool returns an error, politely inform the user and suggest alternatives
- When providing weather information, highlight details relevant to agriculture (precipitation, temperature, humidity)
- Be concise but informative in your responses
- If a user asks about weather without specifying a location, ask them to provide one
- Format responses professionally with clear sections for current conditions and forecasts

Example interactions:
- "What's the weather in London?" → Use tool and provide current weather
- "Weather forecast for New York on 2025-10-05" → Use tool with date parameter
- "Will it rain in Tokyo tomorrow?" → Use tool and focus on precipitation info
"""

# Create the weather tool
weather_tool = FunctionTool(func=get_weather_report)

# Create the weather agent
root_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="weather_agent",
    description="Specialized agent for weather information and forecasts",
    instruction=INSTRUCTION,
    tools=[weather_tool]
)
