"""
Dashboard Agent Tools for Snowflake Database Queries.
Provides intelligent SQL query generation and execution for data retrieval.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from decimal import Decimal
from adk_app.core.database import get_snowflake_manager

logger = logging.getLogger(__name__)


# Database schema information for query generation
DATABASE_SCHEMA = {
    "STG_ML_YIELD_FORECASTS": {
        "description": "ML-based yield forecasts for various crops and districts",
        "columns": {
            "ID": {"type": "NUMBER", "description": "Unique identifier"},
            "DISTRICT_NAME": {"type": "VARCHAR", "description": "District/location name"},
            "CROP_TYPE": {"type": "VARCHAR", "description": "Type of crop variety (e.g., 'High Yielding Variety (HYV) Aman', 'Aman', 'Aus', 'Boro')"},
            "FORECAST_YEAR": {"type": "NUMBER", "description": "Year of forecast (e.g., 2024, 2025, 2026)"},
            "PREDICTED_YIELD": {"type": "NUMBER", "description": "ML-predicted yield value in tons per hectare"},
            "CONFIDENCE_LOWER": {"type": "NUMBER", "description": "Lower confidence bound"},
            "CONFIDENCE_UPPER": {"type": "NUMBER", "description": "Upper confidence bound"},
            "MODEL_USED": {"type": "VARCHAR", "description": "ML model name (e.g., 'Ensemble')"},
            "PREDICTION_DATE": {"type": "DATE", "description": "When prediction was made"},
            "HISTORICAL_YIELDS": {"type": "VARIANT", "description": "Historical yield data (JSON)"},
            "MODEL_METRICS": {"type": "VARIANT", "description": "Model performance metrics (JSON)"}
        },
        "sample_queries": [
            "Show me yield forecasts for Dhaka district",
            "What are the predicted yields for Aman crop in 2025?",
            "List all forecasts with yield above 3 tons per hectare",
            "Show me the latest predictions by district"
        ]
    },
    "VW_STG_CROP_PRACTICE": {
        "description": "Crop cultivation best practices and variety information",
        "columns": {
            "CROP_PRACTICE_ID": {"type": "NUMBER", "description": "Unique identifier"},
            "CROP_TYPE": {"type": "VARCHAR", "description": "Crop type (e.g., 'rice', 'wheat', 'maize')"},
            "VARIETY": {"type": "VARCHAR", "description": "Specific variety name (e.g., 'BRRI dhan29', 'BR3')"},
            "RELEASE_YEAR": {"type": "NUMBER", "description": "Year variety was released"},
            "GRAIN_TYPE": {"type": "VARCHAR", "description": "Grain characteristics"},
            "PLANT_HEIGHT_FROM_CM": {"type": "NUMBER", "description": "Minimum plant height in cm"},
            "PLANT_HEIGHT_TO_CM": {"type": "NUMBER", "description": "Maximum plant height in cm"},
            "GRAIN_YIELD_FROM_T_HA": {"type": "NUMBER", "description": "Minimum expected yield in tons per hectare"},
            "GRAIN_YIELD_TO_T_HA": {"type": "NUMBER", "description": "Maximum expected yield in tons per hectare"},
            "DURATION_FROM_DAYS": {"type": "NUMBER", "description": "Minimum growth duration in days"},
            "DURATION_TO_DAYS": {"type": "NUMBER", "description": "Maximum growth duration in days"},
            "GRAINS_PER_SPIKE": {"type": "NUMBER", "description": "Number of grains per spike"},
            "GRAIN_WEIGHT_1000_G": {"type": "NUMBER", "description": "Weight of 1000 grains in grams"},
            "SEASON": {"type": "VARCHAR", "description": "Growing season (e.g., 'Aman', 'Boro', 'Aus', 'Rabi', 'Kharif')"},
            "RESISTANT_TO": {"type": "VARCHAR", "description": "Disease/pest resistance"},
            "SUITABLE_FOR": {"type": "VARCHAR", "description": "Suitable growing conditions"},
            "NOTE": {"type": "VARCHAR", "description": "Additional notes and recommendations"}
        },
        "sample_queries": [
            "Show me rice varieties for Aman season",
            "What varieties have yield above 6 tons per hectare?",
            "List varieties resistant to blast disease",
            "Show me all varieties released after 2000"
        ]
    }
}


def _convert_decimal(obj):
    """Convert Decimal objects to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def _format_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Format query results for JSON serialization."""
    formatted_results = []
    for row in results:
        formatted_row = {}
        for key, value in row.items():
            if isinstance(value, (datetime, date)):
                formatted_row[key.lower()] = value.isoformat()
            elif isinstance(value, Decimal):
                formatted_row[key.lower()] = float(value)
            else:
                formatted_row[key.lower()] = value
        formatted_results.append(formatted_row)
    return formatted_results


def get_database_schema() -> Dict[str, Any]:
    """
    Get the database schema information for available tables.
    
    This tool provides information about available tables, their columns,
    data types, and descriptions to help understand what data can be queried.
    
    Returns:
        Dictionary containing schema information for all available tables
        
    Example:
        User: "What tables are available in the database?"
        Agent: [Calls this tool to show available tables and their structure]
    """
    try:
        return {
            "status": "success",
            "database": "DEV_DATA_ML_DB",
            "schema": "DATA_ML_SCHEMA",
            "tables": DATABASE_SCHEMA,
            "note": "Use this schema information to understand what data is available and how to query it."
        }
    except Exception as e:
        logger.error(f"Error getting database schema: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to get schema: {str(e)}"
        }


def generate_and_execute_query(
    user_query: str,
    table_name: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Generate and execute a SQL query based on natural language user query.
    
    This tool uses LLM-powered query generation to convert user questions into
    safe, read-only SQL queries and executes them against the Snowflake database.
    
    IMPORTANT: This tool only generates SELECT queries (read-only).
    No INSERT, UPDATE, DELETE, or DDL operations are allowed.
    
    Args:
        user_query: Natural language query from user
                   Examples: 
                   - "Show me all yield forecasts for Dhaka"
                   - "What are the top 5 highest predicted yields?"
                   - "List rice varieties for Aman season"
        table_name: Optional table name to query (if not specified, will be inferred)
                   Options: "STG_ML_YIELD_FORECASTS", "VW_STG_CROP_PRACTICE"
        limit: Maximum number of records to return (default: 50, max: 100)
    
    Returns:
        Dictionary containing query results and metadata
        
    Example:
        User: "Show me yield forecasts for Dhaka district in 2025"
        Agent: [Calls this tool with user_query="Show me yield forecasts for Dhaka district in 2025"]
    """
    try:
        # Validate limit
        if limit > 100:
            limit = 100
            logger.warning("Limit capped at 100 records")
        
        # Infer table name if not provided
        if not table_name:
            table_name = _infer_table_name(user_query)
        
        # Validate table name
        if table_name not in DATABASE_SCHEMA:
            return {
                "status": "error",
                "error_message": f"Invalid table name: {table_name}",
                "available_tables": list(DATABASE_SCHEMA.keys()),
                "suggestion": "Please specify a valid table name or let me infer it from your query."
            }
        
        # Generate SQL query
        sql_query = _generate_sql_query(user_query, table_name, limit)
        
        # Validate query is read-only
        if not _is_read_only_query(sql_query):
            return {
                "status": "error",
                "error_message": "Only SELECT queries are allowed. No data modification permitted.",
                "suggestion": "Please rephrase your query to retrieve data only."
            }
        
        # Execute query
        manager = get_snowflake_manager()
        logger.info(f"Executing generated query: {sql_query}")
        
        results = manager.execute_query(sql_query)
        
        if not results:
            return {
                "status": "success",
                "message": "Query executed successfully but returned no results.",
                "query": sql_query,
                "table": table_name,
                "count": 0,
                "results": []
            }
        
        # Format results
        formatted_results = _format_results(results)
        
        return {
            "status": "success",
            "count": len(formatted_results),
            "query": sql_query,
            "table": table_name,
            "results": formatted_results,
            "source": "Snowflake Database",
            "database": "DEV_DATA_ML_DB.DATA_ML_SCHEMA",
            "note": "Query executed successfully. Results are limited to ensure performance."
        }
        
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return {
            "status": "error",
            "error_type": "query_execution_error",
            "error_message": f"Failed to execute query: {str(e)}",
            "suggestion": "Please rephrase your query or check the database schema."
        }


def _infer_table_name(user_query: str) -> str:
    """Infer the most appropriate table name from user query."""
    query_lower = user_query.lower()
    
    # Strong indicators for crop practice table (check these first)
    practice_strong = ['variety', 'varieties', 'cultivation', 'resistant', 'resistance', 
                      'plant height', 'duration', 'grain weight', 'release year', 'suitable for']
    
    # Check for strong practice indicators first
    for keyword in practice_strong:
        if keyword in query_lower:
            return "VW_STG_CROP_PRACTICE"
    
    # Keywords for yield forecasts table
    yield_keywords = ['forecast', 'predict', 'predicted', 'ml', 'model', 'confidence']
    
    # Keywords for crop practice table (weaker indicators)
    practice_keywords = ['practice', 'season', 'grain', 'brri']
    
    # Count keyword matches
    yield_score = sum(1 for keyword in yield_keywords if keyword in query_lower)
    practice_score = sum(1 for keyword in practice_keywords if keyword in query_lower)
    
    # Return table with higher score
    if practice_score > yield_score:
        return "VW_STG_CROP_PRACTICE"
    else:
        return "STG_ML_YIELD_FORECASTS"


def _generate_sql_query(user_query: str, table_name: str, limit: int) -> str:
    """
    Generate SQL query from natural language query.
    
    This is a simplified implementation. In production, you would use
    an LLM to generate more sophisticated queries.
    """
    query_lower = user_query.lower()
    schema = DATABASE_SCHEMA[table_name]
    
    # Base query
    full_table_name = f"DEV_DATA_ML_DB.DATA_ML_SCHEMA.{table_name}"
    
    # Start with SELECT *
    sql = f"SELECT * FROM {full_table_name}"
    
    # Add WHERE clauses based on common patterns
    where_clauses = []
    
    if table_name == "STG_ML_YIELD_FORECASTS":
        # Extract district
        for word in query_lower.split():
            if word.capitalize() in ['Dhaka', 'Bagerhat', 'Chittagong', 'Mymensingh', 'Bandarban', 'Barguna', 'Barisal', 'Bhola']:
                where_clauses.append(f"LOWER(DISTRICT_NAME) = '{word.lower()}'")
        
        # Extract crop type
        if 'aman' in query_lower:
            where_clauses.append("LOWER(CROP_TYPE) LIKE '%aman%'")
        elif 'aus' in query_lower:
            where_clauses.append("LOWER(CROP_TYPE) LIKE '%aus%'")
        elif 'boro' in query_lower:
            where_clauses.append("LOWER(CROP_TYPE) LIKE '%boro%'")
        
        # Extract year
        for word in query_lower.split():
            if word.isdigit() and len(word) == 4:
                year = int(word)
                if 2020 <= year <= 2030:
                    where_clauses.append(f"FORECAST_YEAR = {year}")
        
        # Handle yield comparisons
        if 'above' in query_lower or 'greater than' in query_lower or '>' in query_lower:
            # Extract number
            words = query_lower.replace('>', ' ').split()
            for i, word in enumerate(words):
                if word.replace('.', '').isdigit():
                    threshold = float(word)
                    where_clauses.append(f"PREDICTED_YIELD > {threshold}")
                    break
        
        # Default ordering
        order_by = "ORDER BY PREDICTION_DATE DESC, FORECAST_YEAR DESC"
    
    elif table_name == "VW_STG_CROP_PRACTICE":
        # Extract season
        if 'aman' in query_lower:
            where_clauses.append("LOWER(SEASON) LIKE '%aman%'")
        elif 'aus' in query_lower:
            where_clauses.append("LOWER(SEASON) LIKE '%aus%'")
        elif 'boro' in query_lower:
            where_clauses.append("LOWER(SEASON) LIKE '%boro%'")
        
        # Extract crop type
        if 'rice' in query_lower:
            where_clauses.append("LOWER(CROP_TYPE) LIKE '%rice%'")
        elif 'wheat' in query_lower:
            where_clauses.append("LOWER(CROP_TYPE) LIKE '%wheat%'")
        
        # Handle yield comparisons
        if 'above' in query_lower or 'greater than' in query_lower:
            words = query_lower.split()
            for i, word in enumerate(words):
                if word.replace('.', '').isdigit():
                    threshold = float(word)
                    where_clauses.append(f"GRAIN_YIELD_FROM_T_HA > {threshold}")
                    break
        
        # Default ordering
        order_by = "ORDER BY GRAIN_YIELD_FROM_T_HA DESC"
    else:
        order_by = ""
    
    # Add WHERE clause if any conditions
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    
    # Add ordering
    if order_by:
        sql += f" {order_by}"
    
    # Add limit
    sql += f" LIMIT {limit}"
    
    return sql


def _is_read_only_query(sql_query: str) -> bool:
    """Validate that query is read-only (SELECT only)."""
    sql_upper = sql_query.upper().strip()
    
    # Must start with SELECT
    if not sql_upper.startswith('SELECT'):
        return False
    
    # Forbidden keywords
    forbidden_keywords = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE'
    ]
    
    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            return False
    
    return True


def get_table_summary(table_name: str) -> Dict[str, Any]:
    """
    Get summary statistics for a specific table.
    
    Args:
        table_name: Name of the table to summarize
                   Options: "STG_ML_YIELD_FORECASTS", "VW_STG_CROP_PRACTICE"
    
    Returns:
        Dictionary containing summary statistics
        
    Example:
        User: "Give me a summary of the yield forecasts table"
        Agent: [Calls this tool with table_name="STG_ML_YIELD_FORECASTS"]
    """
    try:
        # Validate table name
        if table_name not in DATABASE_SCHEMA:
            return {
                "status": "error",
                "error_message": f"Invalid table name: {table_name}",
                "available_tables": list(DATABASE_SCHEMA.keys())
            }
        
        manager = get_snowflake_manager()
        full_table_name = f"DEV_DATA_ML_DB.DATA_ML_SCHEMA.{table_name}"
        
        # Get row count
        count_query = f"SELECT COUNT(*) as total_rows FROM {full_table_name}"
        count_result = manager.execute_query(count_query, fetch_all=False)
        total_rows = count_result[0]['TOTAL_ROWS'] if count_result else 0
        
        # Get table-specific statistics
        if table_name == "STG_ML_YIELD_FORECASTS":
            stats_query = f"""
            SELECT 
                COUNT(DISTINCT DISTRICT_NAME) as unique_districts,
                COUNT(DISTINCT CROP_TYPE) as unique_crop_types,
                COUNT(DISTINCT FORECAST_YEAR) as unique_years,
                MIN(PREDICTED_YIELD) as min_yield,
                MAX(PREDICTED_YIELD) as max_yield,
                AVG(PREDICTED_YIELD) as avg_yield,
                MIN(FORECAST_YEAR) as earliest_year,
                MAX(FORECAST_YEAR) as latest_year
            FROM {full_table_name}
            """
        elif table_name == "VW_STG_CROP_PRACTICE":
            stats_query = f"""
            SELECT 
                COUNT(DISTINCT CROP_TYPE) as unique_crop_types,
                COUNT(DISTINCT VARIETY) as unique_varieties,
                COUNT(DISTINCT SEASON) as unique_seasons,
                MIN(GRAIN_YIELD_FROM_T_HA) as min_yield,
                MAX(GRAIN_YIELD_TO_T_HA) as max_yield,
                AVG(GRAIN_YIELD_FROM_T_HA) as avg_yield_from,
                MIN(RELEASE_YEAR) as earliest_release,
                MAX(RELEASE_YEAR) as latest_release
            FROM {full_table_name}
            """
        else:
            stats_query = None
        
        stats = {}
        if stats_query:
            stats_result = manager.execute_query(stats_query, fetch_all=False)
            if stats_result:
                stats = _format_results([stats_result[0]])[0]
        
        return {
            "status": "success",
            "table": table_name,
            "total_rows": int(total_rows),
            "statistics": stats,
            "schema": DATABASE_SCHEMA[table_name],
            "source": "Snowflake Database"
        }
        
    except Exception as e:
        logger.error(f"Error getting table summary: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to get table summary: {str(e)}"
        }
