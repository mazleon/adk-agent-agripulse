#!/usr/bin/env python3
"""
Discover all tables in the Snowflake database and their schemas.
This will help us understand what data is available for the dashboard agent.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adk_app.core.database import get_snowflake_manager


def main():
    print("=" * 80)
    print("🔍 Discovering All Snowflake Tables in DATA_ML_SCHEMA")
    print("=" * 80)
    
    manager = get_snowflake_manager()
    
    try:
        # Get all tables in the schema
        print("\n📋 Available Tables:")
        print("-" * 80)
        
        tables_query = """
        SELECT TABLE_NAME, TABLE_TYPE, ROW_COUNT, BYTES
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'DATA_ML_SCHEMA'
        AND TABLE_CATALOG = 'DEV_DATA_ML_DB'
        ORDER BY TABLE_NAME
        """
        
        tables = manager.execute_query(tables_query)
        
        if tables:
            print(f"\nFound {len(tables)} tables/views:\n")
            for table in tables:
                print(f"  📊 {table['TABLE_NAME']}")
                print(f"      Type: {table['TABLE_TYPE']}")
                if table.get('ROW_COUNT'):
                    print(f"      Rows: {table['ROW_COUNT']}")
                print()
        else:
            print("  No tables found")
        
        # Get detailed schema for each table
        print("\n" + "=" * 80)
        print("📝 Detailed Schema Information")
        print("=" * 80)
        
        for table in tables:
            table_name = table['TABLE_NAME']
            print(f"\n{'='*80}")
            print(f"Table: {table_name}")
            print(f"{'='*80}")
            
            # Get columns for this table
            columns_query = f"""
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE, 
                IS_NULLABLE,
                COLUMN_DEFAULT,
                CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'DATA_ML_SCHEMA'
            AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
            """
            
            columns = manager.execute_query(columns_query)
            
            if columns:
                print("\nColumns:")
                for col in columns:
                    nullable = "NULL" if col['IS_NULLABLE'] == 'YES' else "NOT NULL"
                    data_type = col['DATA_TYPE']
                    if col.get('CHARACTER_MAXIMUM_LENGTH'):
                        data_type += f"({col['CHARACTER_MAXIMUM_LENGTH']})"
                    print(f"  • {col['COLUMN_NAME']:<35} {data_type:<20} {nullable}")
            
            # Get sample data
            sample_query = f"SELECT * FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.{table_name} LIMIT 1"
            try:
                sample = manager.execute_query(sample_query, fetch_all=False)
                if sample and len(sample) > 0:
                    print("\nSample Data (first row):")
                    for key, value in sample[0].items():
                        print(f"  • {key:<35} = {value}")
            except Exception as e:
                print(f"\n  ⚠️  Could not fetch sample data: {str(e)}")
        
        print("\n" + "=" * 80)
        print("✅ Schema discovery complete!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        manager.close()


if __name__ == "__main__":
    main()
