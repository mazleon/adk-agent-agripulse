"""
Snowflake-based Yield Prediction Tools.
Fetches real yield forecast data from Snowflake database.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from decimal import Decimal
from adk_app.core.database import get_snowflake_manager

logger = logging.getLogger(__name__)


def _convert_decimal(obj):
    """Convert Decimal objects to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def get_yield_forecast_from_db(
    yield_variety: Optional[str] = None,
    district: Optional[str] = None,
    forecast_year: Optional[int] = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Fetch yield forecasts from Snowflake database.
    
    IMPORTANT: The CROP_TYPE field in database contains the full variety name.
    Examples: "High Yielding Variety (HYV) Aman", "(Broadcast+L.T + HYV) Aman"
    
    Args:
        yield_variety: REQUIRED - Full or partial yield variety name from database
                      Examples: "High Yielding Variety (HYV) Aman", "HYV Aman", "Aman"
        district: REQUIRED - District name (e.g., "Dhaka", "Bagerhat", "Chittagong")
        forecast_year: REQUIRED - Forecast year (e.g., 2024, 2025, 2026)
        limit: Maximum number of records to return (default: 10)
    
    Returns:
        Dictionary containing yield forecast data and metadata
        
    Example:
        # User asks: "rice, HYV Aman, Dhaka, 2025"
        get_yield_forecast_from_db(
            yield_variety="High Yielding Variety (HYV) Aman",
            district="Dhaka",
            forecast_year=2025
        )
        
    Note: 
        - yield_variety should match the actual CROP_TYPE in database
        - Use get_available_crop_types() to see all valid varieties
        - "Rice" is not a valid crop type - use "Aman", "Aus", or "Boro" instead
    """
    try:
        manager = get_snowflake_manager()
        
        # Validate required parameters
        if not yield_variety:
            return {
                "status": "error",
                "error_message": "yield_variety is required. Please specify the crop variety.",
                "suggestion": "Use get_available_crop_types() to see all available varieties. Examples: 'High Yielding Variety (HYV) Aman', 'Aman'"
            }
        
        if not district:
            return {
                "status": "error",
                "error_message": "district is required. Please specify the district name.",
                "suggestion": "Use get_available_districts() to see all available districts. Examples: 'Dhaka', 'Bagerhat'"
            }
        
        if not forecast_year:
            return {
                "status": "error",
                "error_message": "forecast_year is required. Please specify the year.",
                "suggestion": "Use get_available_forecast_years() to see available years. Examples: 2024, 2025, 2026"
            }
        
        # Build query - exact match on year and district, partial match on variety
        query = """
        SELECT 
            ID,
            DISTRICT_NAME,
            CROP_TYPE,
            FORECAST_YEAR,
            PREDICTED_YIELD,
            CONFIDENCE_LOWER,
            CONFIDENCE_UPPER,
            MODEL_USED,
            PREDICTION_DATE
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
        WHERE LOWER(CROP_TYPE) LIKE LOWER(%(yield_variety)s)
          AND LOWER(DISTRICT_NAME) = LOWER(%(district)s)
          AND FORECAST_YEAR = %(forecast_year)s
        ORDER BY PREDICTION_DATE DESC
        LIMIT %(limit)s
        """
        
        params = {
            "yield_variety": f"%{yield_variety}%",
            "district": district,
            "forecast_year": forecast_year,
            "limit": limit
        }
        
        logger.info(f"Executing yield forecast query: variety={yield_variety}, district={district}, year={forecast_year}")
        
        results = manager.execute_query(query, params if params else None)
        
        if not results:
            return {
                "status": "success",
                "message": f"No yield forecasts found for '{yield_variety}' in {district} for year {forecast_year}.",
                "filters_used": {
                    "yield_variety": yield_variety,
                    "district": district,
                    "forecast_year": forecast_year
                },
                "count": 0,
                "forecasts": [],
                "suggestion": "Try:\n1. Use get_available_crop_types() to see exact variety names\n2. Use broader terms like 'Aman' instead of 'HYV Aman'\n3. Check if the district name is correct with get_available_districts()"
            }
        
        # Format results - convert Decimal to float for JSON serialization
        formatted_forecasts = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (datetime, date)):
                    formatted_row[key.lower()] = value.isoformat()
                elif isinstance(value, Decimal):
                    formatted_row[key.lower()] = float(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_forecasts.append(formatted_row)
        
        return {
            "status": "success",
            "count": len(formatted_forecasts),
            "query_parameters": {
                "yield_variety_searched": yield_variety,
                "district": district,
                "forecast_year": forecast_year
            },
            "forecasts": formatted_forecasts,
            "source": "Snowflake ML Database",
            "table": "DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS",
            "note": "Predicted yields are in tons per hectare. Confidence intervals show the range of expected values."
        }
        
    except FileNotFoundError as e:
        logger.error(f"Database configuration error: {str(e)}")
        return {
            "status": "error",
            "error_type": "configuration_error",
            "error_message": str(e),
            "suggestion": "Ensure database_connection_config.pem file exists in the project root"
        }
    
    except Exception as e:
        logger.error(f"Error fetching yield forecasts from database: {str(e)}")
        return {
            "status": "error",
            "error_type": "database_error",
            "error_message": f"Failed to fetch yield forecasts: {str(e)}",
            "suggestion": "Check database connection and credentials"
        }


def get_latest_yield_forecasts(limit: int = 5) -> Dict[str, Any]:
    """
    Get the most recent yield forecasts from the database.
    
    Args:
        limit: Number of recent forecasts to return (default: 5)
    
    Returns:
        Dictionary containing latest yield forecasts
    """
    try:
        manager = get_snowflake_manager()
        
        query = f"""
        SELECT 
            ID,
            DISTRICT_NAME,
            CROP_TYPE,
            FORECAST_YEAR,
            PREDICTED_YIELD,
            CONFIDENCE_LOWER,
            CONFIDENCE_UPPER,
            MODEL_USED,
            PREDICTION_DATE
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
        ORDER BY PREDICTION_DATE DESC, FORECAST_YEAR DESC
        LIMIT {limit}
        """
        
        results = manager.execute_query(query)
        
        if not results:
            return {
                "status": "success",
                "message": "No yield forecasts available",
                "count": 0,
                "forecasts": []
            }
        
        formatted_forecasts = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (datetime, date)):
                    formatted_row[key.lower()] = value.isoformat()
                elif isinstance(value, Decimal):
                    formatted_row[key.lower()] = float(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_forecasts.append(formatted_row)
        
        return {
            "status": "success",
            "count": len(formatted_forecasts),
            "forecasts": formatted_forecasts,
            "source": "Snowflake Database"
        }
        
    except Exception as e:
        logger.error(f"Error fetching latest yield forecasts: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to fetch latest forecasts: {str(e)}"
        }


def get_yield_forecast_summary(
    crop_type: Optional[str] = None,
    district: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get aggregated yield forecast statistics.
    
    Args:
        crop_type: Filter by crop type
        district: Filter by district
    
    Returns:
        Dictionary containing summary statistics
    """
    try:
        manager = get_snowflake_manager()
        
        query = """
        SELECT 
            CROP_TYPE,
            DISTRICT_NAME,
            FORECAST_YEAR,
            COUNT(*) as forecast_count,
            AVG(PREDICTED_YIELD) as avg_predicted_yield,
            MIN(PREDICTED_YIELD) as min_predicted_yield,
            MAX(PREDICTED_YIELD) as max_predicted_yield,
            MAX(PREDICTION_DATE) as latest_prediction_date
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
        WHERE 1=1
        """
        
        params = {}
        
        if crop_type:
            query += " AND LOWER(CROP_TYPE) LIKE LOWER(%(crop_type)s)"
            params["crop_type"] = f"%{crop_type}%"
        
        if district:
            query += " AND LOWER(DISTRICT_NAME) LIKE LOWER(%(district)s)"
            params["district"] = f"%{district}%"
        
        query += " GROUP BY CROP_TYPE, DISTRICT_NAME, FORECAST_YEAR ORDER BY forecast_count DESC"
        
        results = manager.execute_query(query, params if params else None)
        
        if not results:
            return {
                "status": "success",
                "message": "No forecast data available for summary",
                "summary": []
            }
        
        formatted_summary = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (datetime, date)):
                    formatted_row[key.lower()] = value.isoformat()
                elif isinstance(value, Decimal):
                    formatted_row[key.lower()] = float(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_summary.append(formatted_row)
        
        return {
            "status": "success",
            "summary": formatted_summary,
            "filters": {
                "crop_type": crop_type,
                "district": district
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating yield forecast summary: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to generate summary: {str(e)}"
        }


def get_available_crop_types() -> Dict[str, Any]:
    """
    Get list of all available crop types and varieties from the database.
    
    Returns:
        Dictionary containing all unique crop types available for forecasting
        
    Example:
        User: "What crop types are available for forecast?"
        Agent: [Calls this tool to show all available options]
    """
    try:
        manager = get_snowflake_manager()
        
        query = """
        SELECT DISTINCT 
            CROP_TYPE,
            COUNT(*) as forecast_count
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
        GROUP BY CROP_TYPE
        ORDER BY forecast_count DESC, CROP_TYPE
        """
        
        results = manager.execute_query(query)
        
        if not results:
            return {
                "status": "success",
                "message": "No crop types found in database",
                "crop_types": []
            }
        
        # Format results - convert Decimal to float
        formatted_crop_types = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, Decimal):
                    formatted_row[key.lower()] = int(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_crop_types.append(formatted_row)
        
        # Extract unique crop categories
        crop_categories = set()
        for crop in formatted_crop_types:
            crop_name = crop['crop_type']
            # Extract main crop type (e.g., "Aman" from "HYV Aman")
            if 'Aman' in crop_name:
                crop_categories.add('Aman')
            if 'Aus' in crop_name:
                crop_categories.add('Aus')
            if 'Boro' in crop_name:
                crop_categories.add('Boro')
            if 'HYV' in crop_name:
                crop_categories.add('HYV (High Yielding Variety)')
            if 'Local' in crop_name:
                crop_categories.add('Local Variety')
            if 'Broadcast' in crop_name:
                crop_categories.add('Broadcast')
        
        return {
            "status": "success",
            "total_varieties": len(formatted_crop_types),
            "crop_types": formatted_crop_types,
            "main_categories": sorted(list(crop_categories)),
            "source": "Snowflake ML Database",
            "note": "These are all crop types available for yield forecasting in our database"
        }
        
    except Exception as e:
        logger.error(f"Error fetching available crop types: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to fetch crop types: {str(e)}"
        }


def get_available_districts() -> Dict[str, Any]:
    """
    Get list of all available districts/locations from the database.
    
    Returns:
        Dictionary containing all districts with forecast data
        
    Example:
        User: "What districts are covered?"
        Agent: [Calls this tool to show all available districts]
    """
    try:
        manager = get_snowflake_manager()
        
        query = """
        SELECT DISTINCT 
            DISTRICT_NAME,
            COUNT(*) as forecast_count
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
        GROUP BY DISTRICT_NAME
        ORDER BY DISTRICT_NAME
        """
        
        results = manager.execute_query(query)
        
        if not results:
            return {
                "status": "success",
                "message": "No districts found in database",
                "districts": []
            }
        
        # Format results
        formatted_districts = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, Decimal):
                    formatted_row[key.lower()] = int(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_districts.append(formatted_row)
        
        return {
            "status": "success",
            "total_districts": len(formatted_districts),
            "districts": formatted_districts,
            "source": "Snowflake ML Database"
        }
        
    except Exception as e:
        logger.error(f"Error fetching available districts: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to fetch districts: {str(e)}"
        }


def get_available_forecast_years() -> Dict[str, Any]:
    """
    Get list of all available forecast years from the database.
    
    Returns:
        Dictionary containing all years with forecast data
        
    Example:
        User: "What years are available for forecasts?"
        Agent: [Calls this tool to show available years]
    """
    try:
        manager = get_snowflake_manager()
        
        query = """
        SELECT DISTINCT 
            FORECAST_YEAR,
            COUNT(*) as forecast_count
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
        GROUP BY FORECAST_YEAR
        ORDER BY FORECAST_YEAR DESC
        """
        
        results = manager.execute_query(query)
        
        if not results:
            return {
                "status": "success",
                "message": "No forecast years found in database",
                "years": []
            }
        
        # Format results
        formatted_years = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, Decimal):
                    formatted_row[key.lower()] = int(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_years.append(formatted_row)
        
        return {
            "status": "success",
            "total_years": len(formatted_years),
            "years": formatted_years,
            "source": "Snowflake ML Database"
        }
        
    except Exception as e:
        logger.error(f"Error fetching available forecast years: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to fetch forecast years: {str(e)}"
        }


def test_database_connection() -> Dict[str, Any]:
    """
    Test the Snowflake database connection.
    
    Returns:
        Dictionary with connection test results
    """
    try:
        manager = get_snowflake_manager()
        
        if manager.test_connection():
            # Try to query the yield forecasts table
            query = "SELECT COUNT(*) as record_count FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS"
            result = manager.execute_query(query, fetch_all=False)
            
            record_count = result[0].get('RECORD_COUNT', 0) if result else 0
            
            return {
                "status": "success",
                "message": "Database connection successful",
                "database": "DEV_DATA_ML_DB",
                "schema": "DATA_ML_SCHEMA",
                "table": "STG_ML_YIELD_FORECASTS",
                "record_count": record_count
            }
        else:
            return {
                "status": "error",
                "error_message": "Database connection test failed"
            }
            
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Connection test failed: {str(e)}"
        }
