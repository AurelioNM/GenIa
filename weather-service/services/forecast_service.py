from collections import defaultdict
from datetime import date, datetime
import logging
from typing import Dict, List

from clients.dto.open_weather_forecast_dto import (
    ForecastItem,
    OpenWeatherForecastResponse,
)
from models.weather import Weather
from storages.city_storage import CityStorage
from storages.weather_storage import WeatherStorage


class ForecastService:
    def __init__(self, weather_storage: WeatherStorage):
        self.logger = logging.getLogger(__name__)
        self.weather_storage = weather_storage

    async def process_forecast(
        self, city_name: str, forecast: OpenWeatherForecastResponse
    ):
        self.logger.info("Processing forecast")

        filtered_forecasts: List[ForecastItem] = self.filter_forecast_by_day(forecast)

        weather_list: List[Weather] = self.map_forecast_item_to_weather(
            filtered_forecasts
        )

        await self.weather_storage.update_forecast_by_city(city_name, weather_list)

        self.logger.info("Finished processing forecast")

    def filter_forecast_by_day(
        self, forecast: OpenWeatherForecastResponse
    ) -> List[ForecastItem]:
        self.logger.info(f"Filtering forecast: size={forecast.cnt}")

        selected_by_day: Dict[str, ForecastItem] = {}

        for item in forecast.list:
            date_part = item.dt_txt.split(" ")[0]

            # Se ainda não escolheu nada para esse dia, salva o primeiro forecast
            if date_part not in selected_by_day:
                selected_by_day[date_part] = item
                continue

            # Se encontrar um registro de meio-dia, ele tem prioridade, insira ele no lugar do anterior
            if item.dt_txt.endswith("12:00:00"):
                selected_by_day[date_part] = item

        filtered = list(selected_by_day.values())

        self.logger.info(f"Filtered forecast: size={len(filtered)}")

        return filtered

    def map_forecast_item_to_weather(self, items: ForecastItem) -> List[Weather]:
        weather_list: List[Weather] = []

        for item in items:

            day: date = datetime.strptime(item.dt_txt, "%Y-%m-%d %H:%M:%S").date()

            weather = Weather(
                day=day,
                type=self.weather_storage.resolve_weather_type(day),
                description=item.weather[0].description,
                temp=item.main.temp,
                temp_min=item.main.temp_min,
                temp_max=item.main.temp_max,
                feels_like=item.main.feels_like,
                humidity=item.main.humidity,
                wind_speed=item.wind.speed,
            )

            weather_list.append(weather)

        self.logger.info(
            f"Mapped forecast  to model size={len(weather_list)}, result={weather_list}"
        )

        return weather_list
