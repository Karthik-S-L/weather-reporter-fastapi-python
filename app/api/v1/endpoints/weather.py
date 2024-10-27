# app/api/v1/endpoints/weather.py

from fastapi import APIRouter, HTTPException
from app.services.weather_service import fetch_weather  # Import the weather service function

router = APIRouter()

@router.get("/{city}", response_model=dict)
async def get_weather(city: str):
    """
    Fetches weather data for a given city.
    First checks cache; if not found, fetches from OpenWeatherMap API.
    """
    try:
        weather_data = await fetch_weather(city)
        return {"city": city, "weather": weather_data}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Could not fetch weather data")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
