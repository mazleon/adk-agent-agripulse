#!/usr/bin/env python3
"""
Test script to verify correct query behavior.
Tests the scenario from the user's screenshot.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adk_app.tools.snowflake_yield_tools import (
    get_yield_forecast_from_db,
    get_available_crop_types
)


def main():
    print("=" * 80)
    print("🧪 Testing Correct Query Behavior")
    print("=" * 80)
    
    # Scenario from screenshot:
    # User asked for: rice, HYV Aman, Dhaka, 2025, season: aman
    
    print("\n📋 User Request (from screenshot):")
    print("-" * 80)
    print("  - Crop type: rice")
    print("  - Yield variety: High Yielding Variety (HYV) Aman")
    print("  - Location: Dhaka")
    print("  - Time: 2025")
    print("  - Season: aman")
    
    print("\n🔍 Step 1: Show available crop types (what agent should do)")
    print("-" * 80)
    result = get_available_crop_types()
    if result["status"] == "success":
        print(f"Available varieties:")
        for crop in result['crop_types']:
            print(f"  - {crop['crop_type']}")
    
    print("\n❌ Step 2: WRONG - What the agent did before (searching for 'rice')")
    print("-" * 80)
    print("  This would fail because 'rice' is not in the database")
    
    print("\n✅ Step 3: CORRECT - What the agent should do")
    print("-" * 80)
    print("  Query with exact variety name from database:")
    print("  - yield_variety: 'High Yielding Variety (HYV) Aman'")
    print("  - district: 'Dhaka'")
    print("  - forecast_year: 2025")
    
    result = get_yield_forecast_from_db(
        yield_variety="High Yielding Variety (HYV) Aman",
        district="Dhaka",
        forecast_year=2025
    )
    
    if result["status"] == "success" and result["count"] > 0:
        print(f"\n✅ Found {result['count']} forecast(s)!")
        forecast = result['forecasts'][0]
        print(f"\n📊 Forecast Details:")
        print(f"  - Crop Type (from DB): {forecast['crop_type']}")
        print(f"  - District: {forecast['district_name']}")
        print(f"  - Forecast Year: {forecast['forecast_year']}")
        print(f"  - Predicted Yield: {forecast['predicted_yield']:.2f} tons/hectare")
        print(f"  - Confidence Range: {forecast['confidence_lower']:.2f} to {forecast['confidence_upper']:.2f}")
        print(f"  - Model: {forecast['model_used']}")
        
        print(f"\n✅ CORRECT RESPONSE:")
        print(f"  The agent should return:")
        print(f"  - Crop Type: {forecast['crop_type']}")
        print(f"  - NOT: '(Broadcast+L.T + HYV) Aman' when user asked for 'HYV Aman'")
    else:
        print(f"\n❌ No results found")
        print(f"Message: {result.get('message')}")
        print(f"Suggestion: {result.get('suggestion')}")
    
    print("\n" + "=" * 80)
    print("📝 Key Learnings:")
    print("-" * 80)
    print("1. ✅ 'Rice' is too general - must use specific variety")
    print("2. ✅ Season (Aman) is already part of crop type")
    print("3. ✅ Must use exact variety name from database")
    print("4. ✅ Agent should show available varieties first")
    print("5. ✅ Required params: yield_variety, district, forecast_year")
    print("=" * 80)
    
    print("\n🎯 Correct Agent Flow:")
    print("-" * 80)
    print("User: 'I want rice forecast for Dhaka in 2025'")
    print("Agent: [Calls get_available_crop_types()]")
    print("Agent: 'We have these rice varieties: HYV Aman, Broadcast Aman'")
    print("Agent: 'Which one would you like?'")
    print("User: 'HYV Aman'")
    print("Agent: [Calls get_yield_forecast_from_db(")
    print("           yield_variety='High Yielding Variety (HYV) Aman',")
    print("           district='Dhaka',")
    print("           forecast_year=2025")
    print("       )]")
    print("=" * 80)


if __name__ == "__main__":
    main()
