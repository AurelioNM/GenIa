import logging
from typing import List
from langchain_core.tools import StructuredTool

from services.product_service import ProductService
from services.weather_service import WeatherService
from models.product import ProductSummary
from models.weather import Weather
from models.tool_output import (
    SuggestDayAndProductOnWeatherToolOutput,
    SuggestProductToolOutput,
)


class SuggestDayAndProductOnWeatherTool:
    def __init__(
        self, weather_service: WeatherService, product_service: ProductService
    ):
        self.logger = logging.getLogger(__name__)
        self.weather_service = weather_service
        self.product_service = product_service

    def _execute(
        self,
    ) -> SuggestProductToolOutput:
        self.logger.info(f"Executing tool suggest_day_and_product_on_weather")

        forecast: List[Weather] = self.weather_service.get_weather_forecast()
        products: List[ProductSummary] = self.product_service.get_products_by_category(
            "WEATHER"
        )

        return SuggestDayAndProductOnWeatherToolOutput(
            forecast=forecast, products=products
        ).model_dump()

    def get_tool(self):
        return StructuredTool.from_function(
            func=self._execute,
            name="suggest_day_and_product_on_weather",
            description="Get weather forecast and products on weather category. Based on customer weather preference, use to recomend day to go out and products to buy.",
        )
