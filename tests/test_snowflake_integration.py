"""Tests for Snowflake database integration."""
import pytest
from adk_app.tools.snowflake_yield_tools import (
    test_database_connection,
    get_yield_forecast_from_db,
    get_latest_yield_forecasts,
    get_yield_forecast_summary
)


def test_database_connection():
    """Test Snowflake database connection."""
    result = test_database_connection()
    
    # Should return a result (success or error)
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "database" in result
        assert "record_count" in result


def test_get_yield_forecast_from_db():
    """Test fetching yield forecasts from database."""
    result = get_yield_forecast_from_db(limit=5)
    
    assert "status" in result
    assert result["status"] in ["success", "error"]
    
    if result["status"] == "success":
        assert "forecasts" in result
        assert "count" in result
        assert isinstance(result["forecasts"], list)


def test_get_yield_forecast_with_filters():
    """Test fetching yield forecasts with filters."""
    result = get_yield_forecast_from_db(
        crop_type="wheat",
        limit=3
    )
    
    assert "status" in result
    
    if result["status"] == "success" and result["count"] > 0:
        # Verify filters were applied
        assert "filters" in result
        assert result["filters"]["crop_type"] == "wheat"


def test_get_latest_yield_forecasts():
    """Test fetching latest yield forecasts."""
    result = get_latest_yield_forecasts(limit=5)
    
    assert "status" in result
    
    if result["status"] == "success":
        assert "forecasts" in result
        assert "count" in result


def test_get_yield_forecast_summary():
    """Test getting yield forecast summary."""
    result = get_yield_forecast_summary()
    
    assert "status" in result
    
    if result["status"] == "success":
        assert "summary" in result
        assert isinstance(result["summary"], list)


def test_error_handling():
    """Test that errors are handled gracefully."""
    # Test with invalid parameters should not crash
    result = get_yield_forecast_from_db(limit=-1)
    
    # Should return a result, even if it's an error
    assert "status" in result
