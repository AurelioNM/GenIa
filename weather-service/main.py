import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient
from clients.open_weather_client import OpenWeatherClient
from configs.db_conn import get_database_connection
from configs.queue_client import get_queue_client
from routes.weather_router import router as weather_router
from services.forecast_service import ForecastService
from services.weather_service import WeatherService
from storages.city_storage import CityStorage
from storages.weather_storage import WeatherStorage
from queues.sqs_client import SQSClient
from queues.sqs_listener import SQSListener

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    await db_connection.open()

    http_weather_client = AsyncClient()

    queue_client_ctx = await get_queue_client()
    boto_queue_client = await queue_client_ctx.__aenter__()

    sqs_client = SQSClient(boto_queue_client)

    weather_storage = WeatherStorage(db_connection=db_connection)
    city_storage = CityStorage(db_connection=db_connection)
    open_weather_client = OpenWeatherClient(http_weather_client)

    forecast_service = ForecastService(weather_storage)
    weather_service = WeatherService(
        weather_storage, city_storage, open_weather_client, forecast_service, sqs_client
    )

    listener = SQSListener(sqs_client, weather_service)
    task = asyncio.create_task(listener.start())

    yield {
        "weather_service": weather_service,
    }
    logger.info("Shutdown weather-service")
    await db_connection.close()
    await open_weather_client.close()
    await boto_queue_client.close()

    await listener.stop()
    task.cancel()


app = FastAPI(lifespan=lifespan, title="Weather Service")

app.include_router(weather_router)
