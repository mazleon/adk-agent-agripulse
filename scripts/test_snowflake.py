#!/usr/bin/env python3
"""
Test script for Snowflake database integration.
Run this to verify your Snowflake connection is working.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adk_app.tools.snowflake_yield_tools import (
    test_database_connection,
    get_latest_yield_forecasts,
    get_yield_forecast_from_db
)


def main():
    print("=" * 60)
    print("🌾 AgriPulse AI - Snowflake Integration Test")
    print("=" * 60)
    
    # Test 1: Connection
    print("\n1️⃣  Testing database connection...")
    print("-" * 60)
    result = test_database_connection()
    
    if result["status"] == "success":
        print("✅ Connection successful!")
        print(f"   Database: {result.get('database')}")
        print(f"   Schema: {result.get('schema')}")
        print(f"   Table: {result.get('table')}")
        print(f"   Record count: {result.get('record_count')}")
    else:
        print("❌ Connection failed!")
        print(f"   Error: {result.get('error_message')}")
        print(f"   Suggestion: {result.get('suggestion', 'Check credentials')}")
        return
    
    # Test 2: Latest forecasts
    print("\n2️⃣  Fetching latest yield forecasts...")
    print("-" * 60)
    result = get_latest_yield_forecasts(limit=3)
    
    if result["status"] == "success":
        print(f"✅ Retrieved {result['count']} forecasts")
        for i, forecast in enumerate(result['forecasts'], 1):
            print(f"\n   Forecast #{i}:")
            for key, value in list(forecast.items())[:5]:  # Show first 5 fields
                print(f"   - {key}: {value}")
    else:
        print("❌ Failed to fetch forecasts")
        print(f"   Error: {result.get('error_message')}")
    
    # Test 3: Filtered query
    print("\n3️⃣  Testing filtered query (wheat)...")
    print("-" * 60)
    result = get_yield_forecast_from_db(crop_type="wheat", limit=2)
    
    if result["status"] == "success":
        print(f"✅ Retrieved {result['count']} wheat forecasts")
        if result['count'] > 0:
            print("\n   Sample forecast:")
            forecast = result['forecasts'][0]
            for key, value in list(forecast.items())[:5]:
                print(f"   - {key}: {value}")
        else:
            print("   No wheat forecasts found in database")
    else:
        print("❌ Query failed")
        print(f"   Error: {result.get('error_message')}")
    
    print("\n" + "=" * 60)
    print("✅ Snowflake integration test complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run the yield agent: uv run adk run adk_app/agents/yield_agent")
    print("2. Ask: 'Show me the latest yield forecasts'")
    print("3. Ask: 'What's the yield forecast for wheat?'")
    print("=" * 60)


if __name__ == "__main__":
    main()
