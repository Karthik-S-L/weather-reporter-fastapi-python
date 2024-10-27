import os

# API key for OpenWeatherMap
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_default_api_key_here")

if not OPENWEATHER_API_KEY:
    raise ValueError("API key for OpenWeatherMap must be set.")
