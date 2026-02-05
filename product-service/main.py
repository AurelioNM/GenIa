import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from configs.db_conn import get_database_connection
from routes.product_router import router as product_router
from routes.weather_router import router as weather_router
from services.product_service import ProductService
from services.weather_service import WeatherService
from storages.product_storage import ProductStorage
from storages.weather_storage import WeatherStorage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    product_storage = ProductStorage(db_connection=db_connection)
    product_service = ProductService(product_storage)

    weather_storage = WeatherStorage(db_connection=db_connection)
    weather_service = WeatherService(weather_storage)

    yield {"product_service": product_service, "weather_service": weather_service}
    logger.info("Shutdown application")


app = FastAPI(lifespan=lifespan, title="Gen AI Product Service")
app.include_router(product_router)
app.include_router(weather_router)
