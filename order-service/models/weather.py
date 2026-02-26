from datetime import date
from typing import List
from enum import Enum

from pydantic import BaseModel, Field


class WeatherType(str, Enum):
    PAST = "PAST"
    TODAY = "TODAY"
    FUTURE = "FUTURE"


class Weather(BaseModel):
    day: date = Field(description="Day of the weather record")
    type: WeatherType = Field(description="PAST, TODAY or FUTURE")
    description: str = Field(description="Weather description")
    temp: float = Field(description="Current temperature")


class CityWeather(BaseModel):
    city_name: str = Field(description="City name")
    weather: List[Weather] = Field(description="Weather records list")
