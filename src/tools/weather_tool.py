"""
Weather API Tool for fetching weather information.
Uses Open-Meteo API (free weather API, no API key required).
"""
import requests
from typing import Dict, Any
from datetime import datetime


def get_weather_report(location: str, date: str = None) -> Dict[str, Any]:
    """
    Fetches weather information for a specific location and optional date.
    
    Args:
        location: City name or location (e.g., "London", "New York", "Tokyo")
        date: Optional date in YYYY-MM-DD format. If not provided, returns current weather.
    
    Returns:
        Dictionary containing weather information with status, temperature, conditions, etc.
    """
    try:
        # First, get coordinates for the location using geocoding
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocoding_params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        geo_response = requests.get(geocoding_url, params=geocoding_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return {
                "status": "error",
                "error_message": f"Location '{location}' not found. Please check the spelling or try a different location."
            }
        
        # Extract coordinates
        location_data = geo_data["results"][0]
        latitude = location_data["latitude"]
        longitude = location_data["longitude"]
        location_name = location_data["name"]
        country = location_data.get("country", "")
        
        # Fetch weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "timezone": "auto",
            "forecast_days": 7
        }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Parse current weather
        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})
        
        # Weather code interpretation
        weather_code = current.get("weather_code", 0)
        weather_description = _interpret_weather_code(weather_code)
        
        # Build response
        result = {
            "status": "success",
            "location": f"{location_name}, {country}",
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "current_weather": {
                "temperature": f"{current.get('temperature_2m', 'N/A')}°C",
                "feels_like": f"{current.get('apparent_temperature', 'N/A')}°C",
                "humidity": f"{current.get('relative_humidity_2m', 'N/A')}%",
                "wind_speed": f"{current.get('wind_speed_10m', 'N/A')} km/h",
                "precipitation": f"{current.get('precipitation', 0)} mm",
                "conditions": weather_description,
                "time": current.get("time", "")
            }
        }
        
        # Add forecast if requested date is in the future
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d")
                current_date = datetime.now()
                
                if target_date.date() > current_date.date():
                    # Find the date in the forecast
                    dates = daily.get("time", [])
                    if date in dates:
                        idx = dates.index(date)
                        result["forecast"] = {
                            "date": date,
                            "temperature_max": f"{daily['temperature_2m_max'][idx]}°C",
                            "temperature_min": f"{daily['temperature_2m_min'][idx]}°C",
                            "precipitation": f"{daily['precipitation_sum'][idx]} mm",
                            "conditions": _interpret_weather_code(daily['weather_code'][idx])
                        }
                    else:
                        result["forecast_note"] = f"Forecast for {date} is not available (only 7 days ahead)"
            except ValueError:
                result["date_error"] = "Invalid date format. Please use YYYY-MM-DD format."
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather data: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}"
        }


def _interpret_weather_code(code: int) -> str:
    """
    Interprets WMO weather codes into human-readable descriptions.
    
    Args:
        code: WMO weather code
    
    Returns:
        Human-readable weather description
    """
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    return weather_codes.get(code, "Unknown conditions")
