"""Tests for Weather Agent."""
import pytest
from adk_app.tools.weather_tools import get_weather_report


def test_get_weather_report_success():
    """Test weather report retrieval for a valid location."""
    result = get_weather_report("London")
    
    assert result["status"] == "success"
    assert "location" in result
    assert "current_weather" in result
    assert "London" in result["location"]


def test_get_weather_report_invalid_location():
    """Test weather report with invalid location."""
    result = get_weather_report("InvalidCityXYZ123")
    
    assert result["status"] == "error"
    assert "error_message" in result


def test_get_weather_report_with_date():
    """Test weather report with future date."""
    result = get_weather_report("Paris", "2025-10-05")
    
    assert result["status"] == "success"
    # May or may not have forecast depending on date range
    assert "location" in result
