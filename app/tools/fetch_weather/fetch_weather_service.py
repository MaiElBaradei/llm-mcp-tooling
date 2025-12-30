import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class WeatherService:
    ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
        if not self.api_key:
            logger.warning("OPEN_WEATHER_MAP_API_KEY is not set")
        else:
            logger.info("WeatherService initialized")

    def fetch_weather(self, city: str) -> dict:
        try:
            logger.info(f"Fetching weather from API for city: {city}")
            
            if not self.api_key:
                logger.error("OPEN_WEATHER_MAP_API_KEY is not set")
                raise ValueError("OPEN_WEATHER_MAP_API_KEY is not set")
            
            response = requests.get(
                self.ENDPOINT,
                params={
                    "appid": self.api_key,
                    "q": city,
                    "units": "metric"
                },
                timeout=10
            )
            response.raise_for_status()
            logger.info("Weather API request successful")

        except requests.RequestException as e:
            logger.error(f"Error fetching weather from API: {e}", exc_info=True)
            raise

        try:
            data = response.json()
            logger.debug(f"Weather API response received for {city}")
            
            if "main" not in data or "wind" not in data or "weather" not in data:
                logger.error(f"Invalid API response: missing required fields. Response: {data}")
                raise ValueError("Invalid API response: missing required fields")

            result = {
                "city": city,
                "temperature_celsius": data["main"]["temp"],
                "wind_speed_kmh": data["wind"]["speed"] * 3.6,
                "condition": data["weather"][0]["description"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            logger.info(f"Weather data parsed successfully: {result['temperature_celsius']}°C, {result['condition']}")
            return result
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Error parsing weather API response: {e}", exc_info=True)
            raise
