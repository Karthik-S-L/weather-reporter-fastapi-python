import json
import httpx  # Async HTTP client
from app.core.cache import redis  # Import initialized Redis client from core/cache.py
from app.core.config import OPENWEATHER_API_KEY  # Import API key from core/config

async def get_cache(key: str):
    return await redis.get(key)

async def set_cache(key: str, value: str, expire: int = 3600):
    await redis.set(key, value, ex=expire)

async def fetch_weather(city: str):
    # Check Redis cache first
    cached_data = await get_cache(city)
    if cached_data:
        return json.loads(cached_data)

    # Initialize weather data dictionary
    weather_data = {}

    # Create an async HTTP client session to fetch data from OpenWeatherMap
    async with httpx.AsyncClient() as client:
        openweather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
        openweather_response = await client.get(openweather_url)

        # Raise exception if the request fails
        openweather_response.raise_for_status()
        
        openweather_data = openweather_response.json()

    # Store the OpenWeatherMap data in the weather_data dictionary
    weather_data['openweather'] = openweather_data

    # Store the result in Redis cache
    await set_cache(city, json.dumps(weather_data))
    
    return weather_data
