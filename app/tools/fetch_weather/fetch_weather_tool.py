from .fetch_weather_service import WeatherService
from .fetch_weather_schema import (
    FetchWeatherOutput,
    WeatherInfo,
    WeatherAPIMetadata,
)


class FetchWeatherTool:
    """
    Tool: fetch_weather
    -------------------
    Retrieves current weather for a given city.
    """

    def __init__(self):
        self.service = WeatherService()

    def run(self, city: str) -> FetchWeatherOutput:
        result = self.service.fetch_weather(city)

        return{
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
