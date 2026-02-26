import logging
import os
from models.weather import CityWeather

import httpx


class WeatherClient:
    def __init__(self, client_http: httpx):
        self.logger = logging.getLogger(__name__)
        self.client_http = client_http

    def get_weather_by_city(self) -> CityWeather:
        try:
            city = "Rio de Janeiro"
            self.logger.info(f"Getting weather by city={city}")

            url = f"{os.getenv('WEATHER_BASE_URL')}/v1/weathers/cities/{city}"

            response = self.client_http.get(url)

            response.raise_for_status()

            self.logger.info(f"Get weather response: {response}")

            weather = CityWeather(**response.json())

            self.logger.info(f"Mapped response dto: {weather}")

            return weather
        except httpx.RequestError as e:
            self.logger.error(f"Failed to get weather: {e}")
            raise
