"""Tests for Yield Prediction Agent."""
import pytest
from adk_app.tools.yield_tools import predict_yield, analyze_soil_conditions


def test_predict_yield_wheat():
    """Test yield prediction for wheat."""
    result = predict_yield(
        crop_type="wheat",
        field_size_hectares=10.0,
        location="London"
    )
    
    assert result["status"] == "success"
    assert result["crop_type"] == "wheat"
    assert result["field_size_hectares"] == 10.0
    assert "prediction" in result
    assert "recommendations" in result


def test_predict_yield_with_irrigation():
    """Test yield prediction with irrigation."""
    result = predict_yield(
        crop_type="corn",
        field_size_hectares=5.0,
        location="Paris",
        irrigation=True
    )
    
    assert result["status"] == "success"
    assert "prediction" in result


def test_analyze_soil_conditions():
    """Test soil condition analysis."""
    result = analyze_soil_conditions(location="Tokyo")
    
    assert result["status"] == "success"
    assert "analysis" in result
    assert "recommendations" in result
