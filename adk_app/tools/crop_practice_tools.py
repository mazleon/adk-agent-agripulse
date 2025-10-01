"""
Crop Best Practice Tools.
Fetches crop standard/best practices from Snowflake database.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
from adk_app.core.database import get_snowflake_manager

logger = logging.getLogger(__name__)


def _convert_decimal(obj):
    """Convert Decimal objects to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def get_crop_best_practices(
    crop_type: Optional[str] = None,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get crop best practices and standard practices from Snowflake database.
    
    This tool retrieves information about:
    - Plant height and width recommendations
    - Grain yield range
    - Planting density
    - Fertilizer recommendations
    - Other agricultural best practices
    
    Args:
        crop_type: REQUIRED - Type of crop (e.g., "Rice", "Wheat", "Maize", "Aman", "Aus", "Boro")
        season: REQUIRED - Growing season (e.g., "Kharif", "Rabi", "Summer", "Winter", "Monsoon")
    
    Returns:
        Dictionary containing crop best practice information
        
    Example:
        User: "What are the best practices for rice in Kharif season?"
        get_crop_best_practices(crop_type="Rice", season="Kharif")
        
        User: "Tell me about Aman rice cultivation standards"
        get_crop_best_practices(crop_type="Aman", season="Kharif")
    """
    try:
        manager = get_snowflake_manager()
        
        # Validate required parameters
        if not crop_type:
            return {
                "status": "error",
                "error_message": "crop_type is required. Please specify the crop type.",
                "suggestion": "Examples: 'Rice', 'Wheat', 'Maize', 'Aman', 'Aus', 'Boro'. Ask user: 'Which crop are you interested in?'"
            }
        
        if not season:
            return {
                "status": "error",
                "error_message": "season is required. Please specify the growing season.",
                "suggestion": "Examples: 'Kharif', 'Rabi', 'Summer', 'Winter', 'Monsoon'. Ask user: 'Which season are you planning for?'"
            }
        
        # Build query - partial match on crop_type and season
        query = """
        SELECT 
            CROP_TYPE,
            SEASON,
            PLANT_HEIGHT_CM,
            PLANT_WIDTH_CM,
            GRAIN_YIELD_MIN_KG_HA,
            GRAIN_YIELD_MAX_KG_HA,
            PLANTING_DENSITY_PLANTS_M2,
            FERTILIZER_N_KG_HA,
            FERTILIZER_P_KG_HA,
            FERTILIZER_K_KG_HA,
            IRRIGATION_FREQUENCY_DAYS,
            PEST_MANAGEMENT_NOTES,
            HARVEST_TIME_DAYS,
            SOIL_TYPE_RECOMMENDED,
            ADDITIONAL_NOTES
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE
        WHERE LOWER(CROP_TYPE) LIKE LOWER(%(crop_type)s)
          AND LOWER(SEASON) LIKE LOWER(%(season)s)
        ORDER BY CROP_TYPE, SEASON
        """
        
        params = {
            "crop_type": f"%{crop_type}%",
            "season": f"%{season}%"
        }
        
        logger.info(f"Executing crop practice query: crop_type={crop_type}, season={season}")
        
        results = manager.execute_query(query, params)
        
        if not results:
            return {
                "status": "success",
                "message": f"No best practices found for '{crop_type}' in '{season}' season.",
                "filters_used": {
                    "crop_type": crop_type,
                    "season": season
                },
                "count": 0,
                "practices": [],
                "suggestion": "Try:\n1. Check the crop type spelling (e.g., 'Rice', 'Aman', 'Wheat')\n2. Verify the season name (e.g., 'Kharif', 'Rabi', 'Summer')\n3. Use get_available_crop_practice_types() to see all available options"
            }
        
        # Format results - convert Decimal to float for JSON serialization
        formatted_practices = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, (datetime, date)):
                    formatted_row[key.lower()] = value.isoformat()
                elif isinstance(value, Decimal):
                    formatted_row[key.lower()] = float(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_practices.append(formatted_row)
        
        # Create a user-friendly summary
        summary = []
        for practice in formatted_practices:
            crop_summary = {
                "crop": practice.get('crop_type', 'N/A'),
                "season": practice.get('season', 'N/A'),
                "plant_dimensions": {
                    "height_cm": practice.get('plant_height_cm'),
                    "width_cm": practice.get('plant_width_cm')
                },
                "yield_range": {
                    "min_kg_per_hectare": practice.get('grain_yield_min_kg_ha'),
                    "max_kg_per_hectare": practice.get('grain_yield_max_kg_ha'),
                    "description": f"{practice.get('grain_yield_min_kg_ha', 0):.0f} - {practice.get('grain_yield_max_kg_ha', 0):.0f} kg/ha"
                },
                "planting": {
                    "density_plants_per_m2": practice.get('planting_density_plants_m2'),
                    "recommended_soil": practice.get('soil_type_recommended')
                },
                "fertilizer_recommendations": {
                    "nitrogen_kg_per_ha": practice.get('fertilizer_n_kg_ha'),
                    "phosphorus_kg_per_ha": practice.get('fertilizer_p_kg_ha'),
                    "potassium_kg_per_ha": practice.get('fertilizer_k_kg_ha')
                },
                "management": {
                    "irrigation_frequency_days": practice.get('irrigation_frequency_days'),
                    "harvest_time_days": practice.get('harvest_time_days'),
                    "pest_management": practice.get('pest_management_notes')
                },
                "additional_notes": practice.get('additional_notes')
            }
            summary.append(crop_summary)
        
        return {
            "status": "success",
            "count": len(formatted_practices),
            "query_parameters": {
                "crop_type_searched": crop_type,
                "season": season
            },
            "practices": formatted_practices,
            "summary": summary,
            "source": "Snowflake Database",
            "table": "DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE",
            "note": "These are standard best practices for crop cultivation. Actual results may vary based on local conditions."
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
        logger.error(f"Error fetching crop best practices from database: {str(e)}")
        return {
            "status": "error",
            "error_type": "database_error",
            "error_message": f"Failed to fetch crop best practices: {str(e)}",
            "suggestion": "Check database connection and credentials"
        }


def get_available_crop_practice_types() -> Dict[str, Any]:
    """
    Get list of all available crop types and seasons in the crop practice database.
    
    Returns:
        Dictionary containing all unique crop types and seasons available
        
    Example:
        User: "What crops have best practice information?"
        Agent: [Calls this tool to show all available options]
    """
    try:
        manager = get_snowflake_manager()
        
        query = """
        SELECT DISTINCT 
            CROP_TYPE,
            SEASON,
            COUNT(*) as practice_count
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE
        GROUP BY CROP_TYPE, SEASON
        ORDER BY CROP_TYPE, SEASON
        """
        
        results = manager.execute_query(query)
        
        if not results:
            return {
                "status": "success",
                "message": "No crop practice data found in database",
                "crop_types": [],
                "seasons": []
            }
        
        # Format results and extract unique values
        formatted_practices = []
        unique_crops = set()
        unique_seasons = set()
        
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, Decimal):
                    formatted_row[key.lower()] = int(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_practices.append(formatted_row)
            
            unique_crops.add(formatted_row.get('crop_type'))
            unique_seasons.add(formatted_row.get('season'))
        
        return {
            "status": "success",
            "total_combinations": len(formatted_practices),
            "available_crops": sorted(list(unique_crops)),
            "available_seasons": sorted(list(unique_seasons)),
            "crop_season_combinations": formatted_practices,
            "source": "Snowflake Database",
            "note": "These are all crop types and seasons with best practice information available"
        }
        
    except Exception as e:
        logger.error(f"Error fetching available crop practice types: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to fetch crop practice types: {str(e)}"
        }


def get_crop_practice_summary(crop_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a summary of crop practices across all seasons for a specific crop.
    
    Args:
        crop_type: Crop type to summarize (e.g., "Rice", "Aman", "Wheat")
    
    Returns:
        Dictionary containing summary of practices across seasons
    """
    try:
        manager = get_snowflake_manager()
        
        if not crop_type:
            return {
                "status": "error",
                "error_message": "crop_type is required for summary",
                "suggestion": "Specify a crop type like 'Rice', 'Wheat', or 'Aman'"
            }
        
        query = """
        SELECT 
            CROP_TYPE,
            SEASON,
            AVG(PLANT_HEIGHT_CM) as avg_height,
            AVG(PLANT_WIDTH_CM) as avg_width,
            AVG(GRAIN_YIELD_MIN_KG_HA) as avg_min_yield,
            AVG(GRAIN_YIELD_MAX_KG_HA) as avg_max_yield,
            AVG(PLANTING_DENSITY_PLANTS_M2) as avg_density,
            COUNT(*) as practice_count
        FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE
        WHERE LOWER(CROP_TYPE) LIKE LOWER(%(crop_type)s)
        GROUP BY CROP_TYPE, SEASON
        ORDER BY SEASON
        """
        
        params = {"crop_type": f"%{crop_type}%"}
        
        results = manager.execute_query(query, params)
        
        if not results:
            return {
                "status": "success",
                "message": f"No practice data found for '{crop_type}'",
                "summary": []
            }
        
        # Format results
        formatted_summary = []
        for row in results:
            formatted_row = {}
            for key, value in row.items():
                if isinstance(value, Decimal):
                    formatted_row[key.lower()] = float(value)
                else:
                    formatted_row[key.lower()] = value
            formatted_summary.append(formatted_row)
        
        return {
            "status": "success",
            "crop_type": crop_type,
            "summary": formatted_summary,
            "source": "Snowflake Database"
        }
        
    except Exception as e:
        logger.error(f"Error generating crop practice summary: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Failed to generate summary: {str(e)}"
        }
