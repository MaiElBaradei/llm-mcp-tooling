from .fetch_weather_service import WeatherService
from .fetch_weather_schema import (
    FetchWeatherOutput,
    WeatherInfo,
    WeatherAPIMetadata,
)
import logging

logger = logging.getLogger(__name__)


class FetchWeatherTool:
    name = "fetch_weather"
    description = (
        "Retrieves current weather information for a given city. "
        "Returns temperature, wind speed, condition, and metadata."
    )

    def __init__(self):
        self.service = WeatherService()
        logger.info("FetchWeatherTool initialized")

    def run(self, city: str) -> FetchWeatherOutput:
        try:
            logger.info(f"Fetching weather for city: {city}")
            result = self.service.fetch_weather(city)

            response = {
                "data":{
                    "city": city,
                    "temperature_celsius": result["temperature_celsius"],
                    "wind_speed_kmh": result["wind_speed_kmh"],
                    "condition": result["condition"],
                },
                "metadata":{
                    "provider": "OpenWeatherMap",
                    "endpoint": "current_weather",
                    "timestamp": result["timestamp"],
                },
            }
            logger.info(f"Weather fetched successfully for {city}: {result['temperature_celsius']}°C, {result['condition']}")
            return response
        except Exception as e:
            logger.error(f"Error fetching weather for {city}: {e}", exc_info=True)
            raise
