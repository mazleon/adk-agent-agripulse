"""
Test script for crop practice data integration with yield forecasts.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adk_app.tools.snowflake_yield_tools import (
    get_yield_forecast_from_db,
    get_crop_practice_data
)


def test_combined_workflow():
    """Test the combined workflow of yield forecast + crop practice data."""
    print("=" * 80)
    print("Testing Combined Yield Forecast + Crop Practice Workflow")
    print("=" * 80)
    
    # Test parameters
    yield_variety = "High Yielding Variety (HYV) Aman"
    district = "Dhaka"
    forecast_year = 2025
    crop_type = "rice"
    season = "aman"
    
    print(f"\nTest Parameters:")
    print(f"  Yield Variety: {yield_variety}")
    print(f"  District: {district}")
    print(f"  Forecast Year: {forecast_year}")
    print(f"  Crop Type: {crop_type}")
    print(f"  Season: {season}")
    
    # Step 1: Get yield forecast
    print("\n" + "-" * 80)
    print("Step 1: Fetching Yield Forecast from Database")
    print("-" * 80)
    
    forecast_result = get_yield_forecast_from_db(
        yield_variety=yield_variety,
        district=district,
        forecast_year=forecast_year,
        limit=5
    )
    
    print(f"\nForecast Status: {forecast_result.get('status')}")
    if forecast_result.get('status') == 'success':
        print(f"Records Found: {forecast_result.get('count')}")
        if forecast_result.get('forecasts'):
            first_forecast = forecast_result['forecasts'][0]
            print(f"\nFirst Forecast:")
            print(f"  Predicted Yield: {first_forecast.get('predicted_yield')} tons/hectare")
            print(f"  Confidence Range: {first_forecast.get('confidence_lower')} - {first_forecast.get('confidence_upper')}")
            print(f"  Model: {first_forecast.get('model_used')}")
    else:
        print(f"Error: {forecast_result.get('error_message')}")
    
    # Step 2: Get crop practice data
    print("\n" + "-" * 80)
    print("Step 2: Fetching Crop Practice Data from Database")
    print("-" * 80)
    
    practice_result = get_crop_practice_data(
        crop_type=crop_type,
        season=season,
        limit=5
    )
    
    print(f"\nPractice Data Status: {practice_result.get('status')}")
    if practice_result.get('status') == 'success':
        print(f"Records Found: {practice_result.get('count')}")
        if practice_result.get('practices'):
            first_practice = practice_result['practices'][0]
            print(f"\nFirst Practice Record:")
            print(f"  Available Fields: {list(first_practice.keys())}")
            print(f"\nSample Data:")
            for key, value in list(first_practice.items())[:10]:  # Show first 10 fields
                print(f"  {key}: {value}")
    else:
        print(f"Error: {practice_result.get('error_message')}")
    
    # Step 3: Combined presentation
    print("\n" + "=" * 80)
    print("Step 3: Combined Presentation Format")
    print("=" * 80)
    
    if forecast_result.get('status') == 'success' and practice_result.get('status') == 'success':
        print(f"\n📊 **Yield Forecast for {yield_variety} in {district} ({forecast_year}):**\n")
        
        if forecast_result.get('forecasts'):
            fc = forecast_result['forecasts'][0]
            print(f"* From our historical analysis:")
            print(f"  - Predicted Yield: {fc.get('predicted_yield')} tons per hectare")
            print(f"  - Confidence Interval: {fc.get('confidence_lower')} to {fc.get('confidence_upper')} tons per hectare")
        
        if practice_result.get('practices'):
            print(f"\n🌾 **Recommended Cultivation Practices:**\n")
            practice = practice_result['practices'][0]
            for key, value in practice.items():
                if value is not None:
                    print(f"- {key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 80)
    print("Test Complete!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        test_combined_workflow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
