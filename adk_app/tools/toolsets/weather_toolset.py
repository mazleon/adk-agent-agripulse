"""Weather toolset for organizing weather-related tools."""

from google.adk.tools import FunctionTool
from ..weather_tools import get_weather_report


class WeatherToolset:
    """Collection of weather-related tools."""
    
    @staticmethod
    def get_tools():
        """Get all weather tools."""
        return [
            FunctionTool(func=get_weather_report)
        ]
