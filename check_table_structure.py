"""
Check the actual structure of VW_STG_CROP_PRACTICE table.
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adk_app.core.database import get_snowflake_manager

def check_table_structure():
    """Check the actual columns in VW_STG_CROP_PRACTICE table."""
    try:
        manager = get_snowflake_manager()
        
        # Query to get table structure
        query = """
        SELECT *
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE
        LIMIT 1
        """
        
        print("Fetching table structure...")
        results = manager.execute_query(query)
        
        if results:
            print(f"\nTable: VW_STG_CROP_PRACTICE")
            print(f"Total Columns: {len(results[0])}")
            print("\nColumn Names:")
            for i, column_name in enumerate(results[0].keys(), 1):
                print(f"  {i}. {column_name}")
            
            print("\n" + "="*80)
            print("Sample Data (First Row):")
            print("="*80)
            for key, value in results[0].items():
                print(f"{key}: {value}")
        else:
            print("No data found in table")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()
