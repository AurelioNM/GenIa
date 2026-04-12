import logging
import os
from typing import List

from httpx import AsyncClient, RequestError

from clients.dto.open_weather_forecast_dto import OpenWeatherForecastResponse
from models.weather import PagedCityWeather, PagedCityWeatherV2, Weather


class OpenWeatherClient:
    def __init__(self, client_http: AsyncClient):
        self.logger = logging.getLogger(__name__)
        self.client_http = client_http

    async def close(self):
        self.logger.info(f"Closing async httpclient")
        await self.client_http.aclose()

    async def get_city_forecast(self, city_name: str) -> OpenWeatherForecastResponse:
        try:
            self.logger.info(f"Getting weather forecast by name={city_name}")

            url = f"{os.getenv('OPEN_WEATHER_BASE_URL')}/data/2.5/forecast"
            params = {
                "q": city_name,
                "appid": os.getenv("OPEN_WEATHER_API_KEY"),
                "units": "metric",
            }

            response = await self.client_http.get(url, params=params)

            response.raise_for_status()

            self.logger.info(f"Get weather forecast response: {response}")

            forecast = OpenWeatherForecastResponse(**response.json())

            self.logger.info(
                f"Mapped forecast dto: city={forecast.city.name}, weather_size={len(forecast.list)}"
            )

            return forecast
        except RequestError as e:
            self.logger.error(f"Failed to get open weather forecast: {e}")
            raise
