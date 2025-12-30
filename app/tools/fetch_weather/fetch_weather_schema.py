from pydantic import BaseModel
from typing import Dict, Any


class WeatherInfo(BaseModel):
    city: str
    temperature_celsius: float
    wind_speed_kmh: float
    condition: str


class WeatherAPIMetadata(BaseModel):
    provider: str
    endpoint: str
    timestamp: str


class FetchWeatherOutput(BaseModel):
    data: WeatherInfo
    metadata: WeatherAPIMetadata
