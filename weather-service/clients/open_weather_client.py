import logging
import os
from typing import List

import httpx

from clients.dto.open_weather_forecast_dto import OpenWeatherForecastResponse
from models.weather import PagedCityWeather, PagedCityWeatherV2, Weather


class OpenWeatherClient:
    def __init__(self, client_http: httpx):
        self.logger = logging.getLogger(__name__)
        self.client_http = client_http

    def get_city_forecast(self, city_name: str) -> OpenWeatherForecastResponse:
        try:
            self.logger.info(f"Getting weather forecast by name={city_name}")

            url = f"{os.getenv('OPEN_WEATHER_BASE_URL')}/data/2.5/forecast"
            params = {
                "q": city_name,
                "appid": os.getenv("OPEN_WEATHER_API_KEY"),
                "units": "metric",
                "lang": "pt",
            }

            response = self.client_http.get(url, params=params)

            response.raise_for_status()

            self.logger.info(f"Get weather forecast response: {response}")

            forecast = OpenWeatherForecastResponse(**response.json())

            self.logger.info(f"Mapped forecast dto: {forecast}")

            return forecast
        except httpx.RequestError as e:
            self.logger.error(f"Failed to get open weather forecast: {e}")
            raise
