import logging
from typing import List

from models.weather import CityWeather, Weather, WeatherType
from clients.weather_client import WeatherClient


class WeatherService:
    def __init__(
        self,
        weather_client: WeatherClient,
    ):
        self.logger = logging.getLogger(__name__)
        self.weather_client = weather_client

    def get_weather_forecast(self) -> List[Weather]:
        self.logger.info(f"Getting weather forecast")

        weather: CityWeather = self.weather_client.get_weather_by_city()

        return self._filter_forecast(weather)

    def _filter_forecast(self, weather: CityWeather) -> List[Weather]:
        self.logger.info(
            f"Filtering weather forecast for today and next days: size={len(weather.weather)}"
        )
        filtered_forecast: List[Weather] = []

        for weather in weather.weather:
            if weather.type != WeatherType.PAST:
                filtered_forecast.append(weather)

        self.logger.info(
            f"Filtered weather forecast for today and next days: size={len(filtered_forecast)}, forecast={filtered_forecast}"
        )
        return filtered_forecast
