import logging

from clients.dto.open_weather_forecast_dto import OpenWeatherForecastResponse
from clients.open_weather_client import OpenWeatherClient
from models.weather import PagedCityWeather, PagedCityWeatherV2, Weather
from services.forecast_service import ForecastService
from storages.city_storage import CityStorage
from storages.weather_storage import WeatherStorage


class WeatherService:
    def __init__(
        self,
        weather_storage: WeatherStorage,
        city_storage: CityStorage,
        open_weather_client: OpenWeatherClient,
        forecast_service: ForecastService,
    ):
        self.logger = logging.getLogger(__name__)
        self.weather_storage = weather_storage
        self.city_storage = city_storage
        self.open_weather_client = open_weather_client
        self.forecast_service = forecast_service

    def get_weather_by_city_name(self, city_name: str) -> Weather:
        self.logger.info("Getting weather by city_name")
        return self.weather_storage.get_weather_by_city_name(city_name)

    def get_cities_weather(self, page: int, size: int) -> PagedCityWeather:
        self.logger.info("Getting cities weather by page and size")
        return self.weather_storage.get_paged_cities_weather(page, size)

    def get_cities_weather_v2(self, page: int, size: int) -> PagedCityWeatherV2:
        self.logger.info("Getting cities weather v2 by page and size")
        return self.weather_storage.get_paged_cities_weather_v2(page, size)

    def run_job(self):
        self.logger.info("Running job")

        cities_list = self.city_storage.get_all_cities_names()

        for city_name in cities_list:
            forecast: OpenWeatherForecastResponse = (
                self.open_weather_client.get_city_forecast(city_name)
            )

            self.forecast_service.process_forecast(city_name, forecast)
