#!/usr/bin/env python3
"""
Test script for discovery tools (crop types, districts, years).
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adk_app.tools.snowflake_yield_tools import (
    get_available_crop_types,
    get_available_districts,
    get_available_forecast_years
)


def main():
    print("=" * 70)
    print("🔍 Testing Discovery Tools")
    print("=" * 70)
    
    # Test 1: Get available crop types
    print("\n1️⃣  Testing get_available_crop_types()...")
    print("-" * 70)
    result = get_available_crop_types()
    
    if result["status"] == "success":
        print(f"✅ Found {result['total_varieties']} crop varieties")
        print(f"\n📋 Main Categories:")
        for category in result['main_categories']:
            print(f"   - {category}")
        
        print(f"\n📊 Top 5 Crop Types by Forecast Count:")
        for i, crop in enumerate(result['crop_types'][:5], 1):
            print(f"   {i}. {crop['crop_type']:<50} ({crop['forecast_count']} forecasts)")
    else:
        print(f"❌ Error: {result.get('error_message')}")
    
    # Test 2: Get available districts
    print("\n2️⃣  Testing get_available_districts()...")
    print("-" * 70)
    result = get_available_districts()
    
    if result["status"] == "success":
        print(f"✅ Found {result['total_districts']} districts")
        print(f"\n📍 All Districts:")
        for district in result['districts']:
            print(f"   - {district['district_name']:<30} ({district['forecast_count']} forecasts)")
    else:
        print(f"❌ Error: {result.get('error_message')}")
    
    # Test 3: Get available forecast years
    print("\n3️⃣  Testing get_available_forecast_years()...")
    print("-" * 70)
    result = get_available_forecast_years()
    
    if result["status"] == "success":
        print(f"✅ Found {result['total_years']} forecast years")
        print(f"\n📅 Available Years:")
        for year in result['years']:
            print(f"   - {year['forecast_year']}: {year['forecast_count']} forecasts")
    else:
        print(f"❌ Error: {result.get('error_message')}")
    
    print("\n" + "=" * 70)
    print("✅ Discovery tools test complete!")
    print("=" * 70)
    print("\nThese tools help users discover what data is available.")
    print("\nExample queries:")
    print("  - 'What crop types are available?'")
    print("  - 'What districts are covered?'")
    print("  - 'What years have forecasts?'")
    print("=" * 70)


if __name__ == "__main__":
    main()
