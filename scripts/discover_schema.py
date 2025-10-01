#!/usr/bin/env python3
"""
Discover the actual schema of the Snowflake yield forecasts table.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adk_app.core.database import get_snowflake_manager


def main():
    print("=" * 60)
    print("🔍 Discovering Snowflake Table Schema")
    print("=" * 60)
    
    manager = get_snowflake_manager()
    
    try:
        # Get table columns
        print("\n📋 Table Columns:")
        print("-" * 60)
        
        query = """
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'DATA_ML_SCHEMA'
        AND TABLE_NAME = 'STG_ML_YIELD_FORECASTS'
        ORDER BY ORDINAL_POSITION
        """
        
        columns = manager.execute_query(query)
        
        if columns:
            for col in columns:
                print(f"  - {col['COLUMN_NAME']:<30} {col['DATA_TYPE']:<15} {'NULL' if col['IS_NULLABLE'] == 'YES' else 'NOT NULL'}")
        else:
            print("  No columns found")
        
        # Get sample data
        print("\n📊 Sample Data (first row):")
        print("-" * 60)
        
        sample_query = "SELECT * FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS LIMIT 1"
        sample = manager.execute_query(sample_query, fetch_all=False)
        
        if sample and len(sample) > 0:
            for key, value in sample[0].items():
                print(f"  - {key:<30} = {value}")
        else:
            print("  No data found")
        
        # Get row count
        print("\n📈 Table Statistics:")
        print("-" * 60)
        
        count_query = "SELECT COUNT(*) as total_rows FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS"
        count_result = manager.execute_query(count_query, fetch_all=False)
        
        if count_result:
            print(f"  Total rows: {count_result[0]['TOTAL_ROWS']}")
        
        print("\n" + "=" * 60)
        print("✅ Schema discovery complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        manager.close()


if __name__ == "__main__":
    main()
