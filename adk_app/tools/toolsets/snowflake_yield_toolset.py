"""Snowflake yield prediction toolset for database-backed forecasts."""

from google.adk.tools import FunctionTool
from ..snowflake_yield_tools import (
    get_yield_forecast_from_db,
    get_latest_yield_forecasts,
    get_yield_forecast_summary,
    test_database_connection
)


class SnowflakeYieldToolset:
    """Collection of Snowflake-based yield prediction tools."""
    
    @staticmethod
    def get_tools():
        """Get all Snowflake yield prediction tools."""
        return [
            FunctionTool(func=get_yield_forecast_from_db),
            FunctionTool(func=get_latest_yield_forecasts),
            FunctionTool(func=get_yield_forecast_summary),
            FunctionTool(func=test_database_connection)
        ]
