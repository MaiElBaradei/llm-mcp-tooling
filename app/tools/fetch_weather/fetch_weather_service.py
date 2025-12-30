import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()


class WeatherService:
    ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

    def fetch_weather(self, city: str) -> dict:
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

        data = response.json()

        return {
            "city": city,
            "temperature_celsius": data["main"]["temp"],
            "wind_speed_kmh": data["wind"]["speed"] * 3.6,
            "condition": data["weather"][0]["description"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
