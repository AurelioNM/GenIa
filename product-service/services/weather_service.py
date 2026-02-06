import logging
from typing import List

from clients.open_weather_client import OpenWeatherClient
from models.weather import PagedCityWeather, PagedCityWeatherV2, Weather
from storages.weather_storage import WeatherStorage


class WeatherService:
    def __init__(self, storage: WeatherStorage, open_weather_client: OpenWeatherClient):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        self.open_weather_client = open_weather_client
        self.MINIMUM_PRICE = 1.0

    def get_weather_by_city_name(self, city_name: str) -> Weather:
        self.logger.info("Getting weather by city_name")
        return self.storage.get_weather_by_city_name(city_name)

    def get_cities_weather(self, page: int, size: int) -> PagedCityWeather:
        self.logger.info("Getting cities weather by page and size")
        return self.storage.get_paged_cities_weather(page, size)

    def get_cities_weather_v2(self, page: int, size: int) -> PagedCityWeatherV2:
        self.logger.info("Getting cities weather v2 by page and size")
        return self.storage.get_paged_cities_weather_v2(page, size)

    def run_job(self):
        self.logger.info("Running job")
        return self.open_weather_client.get_city_forecast("Fortaleza")
