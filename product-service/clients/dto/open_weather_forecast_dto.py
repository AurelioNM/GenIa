from pydantic import BaseModel
from typing import List


class WeatherDescription(BaseModel):
    main: str
    description: str


class WeatherMain(BaseModel):
    temp: float
    temp_min: float
    temp_max: float
    feels_like: float
    humidity: int


class Wind(BaseModel):
    speed: float


class ForecastItem(BaseModel):
    dt: int
    main: WeatherMain
    weather: List[WeatherDescription]
    wind: Wind
    dt_txt: str


class City(BaseModel):
    name: str
    timezone: int


class OpenWeatherForecastResponse(BaseModel):
    cnt: int
    list: List[ForecastItem]
    city: City
