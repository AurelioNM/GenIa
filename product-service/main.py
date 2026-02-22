import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from clients.open_weather_client import OpenWeatherClient
from configs.db_conn import get_database_connection
from routes.product_router import router as product_router
from routes.weather_router import router as weather_router
from routes.suggestion_router import router as suggestion_router
from services.forecast_service import ForecastService
from services.product_service import ProductService
from services.suggestion_service import SuggestionService
from services.weather_service import WeatherService
from storages.city_storage import CityStorage
from storages.product_storage import ProductStorage
from storages.weather_storage import WeatherStorage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    # Product
    product_storage = ProductStorage(db_connection=db_connection)
    product_service = ProductService(product_storage)

    # Weather
    weather_storage = WeatherStorage(db_connection=db_connection)
    city_storage = CityStorage(db_connection=db_connection)
    open_weather_client = OpenWeatherClient(httpx)
    forecast_service = ForecastService(weather_storage)
    weather_service = WeatherService(
        weather_storage, city_storage, open_weather_client, forecast_service
    )

    # LLM
    llm = ChatOllama(
        model="llama3",
        temperature=0.0,
        base_url=os.getenv("OLLAMA_BASE_URL"),
        # format="json",  # improves structured reliability
    )
    llm_client = LlmClient(llm=llm)
    suggestion_service = SuggestionService(llm_client=llm_client)

    yield {
        "product_service": product_service,
        "weather_service": weather_service,
        "suggestion_service": suggestion_service,
    }
    logger.info("Shutdown application")


app = FastAPI(lifespan=lifespan, title="Gen AI Product Service")

app.include_router(product_router)
app.include_router(weather_router)
app.include_router(suggestion_router)
