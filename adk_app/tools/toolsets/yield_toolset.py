"""Yield prediction toolset for organizing agricultural tools."""

from google.adk.tools import FunctionTool
from ..yield_tools import predict_yield, analyze_soil_conditions
from ..snowflake_yield_tools import (
    get_yield_forecast_from_db,
    get_latest_yield_forecasts,
    get_yield_forecast_summary,
    get_available_crop_types,
    get_available_districts,
    get_available_forecast_years,
    get_crop_practice_data
)


class YieldToolset:
    """Collection of yield prediction and agricultural tools."""
    
    @staticmethod
    def get_tools():
        """Get all yield prediction tools (both calculated and database-backed)."""
        return [
            # Calculated predictions
            FunctionTool(func=predict_yield),
            FunctionTool(func=analyze_soil_conditions),
            # Database-backed forecasts
            FunctionTool(func=get_yield_forecast_from_db),
            FunctionTool(func=get_latest_yield_forecasts),
            FunctionTool(func=get_yield_forecast_summary),
            # Crop practice recommendations
            FunctionTool(func=get_crop_practice_data),
            # Database metadata/discovery tools
            FunctionTool(func=get_available_crop_types),
            FunctionTool(func=get_available_districts),
            FunctionTool(func=get_available_forecast_years)
        ]
