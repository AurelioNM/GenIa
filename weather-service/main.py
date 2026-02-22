import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from clients.open_weather_client import OpenWeatherClient
from configs.db_conn import get_database_connection
from routes.weather_router import router as weather_router
from services.forecast_service import ForecastService
from services.weather_service import WeatherService
from storages.city_storage import CityStorage
from storages.weather_storage import WeatherStorage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    # Weather
    weather_storage = WeatherStorage(db_connection=db_connection)
    city_storage = CityStorage(db_connection=db_connection)
    open_weather_client = OpenWeatherClient(httpx)
    forecast_service = ForecastService(weather_storage)
    weather_service = WeatherService(
        weather_storage, city_storage, open_weather_client, forecast_service
    )

    yield {
        "weather_service": weather_service,
    }
    logger.info("Shutdown weather-service")


app = FastAPI(lifespan=lifespan, title="Weather Service")

app.include_router(weather_router)
