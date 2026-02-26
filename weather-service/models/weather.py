from datetime import date
from enum import Enum
from typing import List
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
    temp_min: float = Field(description="Minimum temperature")
    temp_max: float = Field(description="Maximum temperature")
    feels_like: float = Field(description="Thermal sensation")
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(ge=0, description="Wind speed")


class CityWeather(BaseModel):
    city_id: str = Field(description="City ULID")
    city_name: str = Field(description="City name")
    weather: List[Weather] = Field(description="Weather records list")


class PagedCityWeather(BaseModel):
    page: int = Field(description="Page number")
    size: int = Field(description="Page size")
    has_next_page: bool = Field(description="If has next page")
    cities_weather: List[CityWeather] = Field(description="Cities weather records list")


class WeatherV2(BaseModel):
    city_id: str = Field(description="City ULID")
    city_name: str = Field(description="City name")
    day: date = Field(description="Day of the weather record")
    type: WeatherType = Field(description="PAST, TODAY or FUTURE")
    description: str = Field(description="Weather description")
    temp: float = Field(description="Current temperature")
    temp_min: float = Field(description="Minimum temperature")
    temp_max: float = Field(description="Maximum temperature")
    feels_like: float = Field(description="Thermal sensation")
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(ge=0, description="Wind speed")


class PagedCityWeatherV2(BaseModel):
    page: int = Field(description="Page number")
    size: int = Field(description="Page size")
    has_next_page: bool = Field(description="If has next page")
    cities_weather: List[WeatherV2] = Field(description="Cities weather records list")
