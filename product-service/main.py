import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from configs.db_conn import get_database_connection
from routes.product_router import router as product_router
from services.product_service import ProductService

from storages.product_storage import ProductStorage


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    product_storage = ProductStorage(db_connection=db_connection)
    product_service = ProductService(product_storage)

    yield {
        "product_service": product_service,
    }
    logger.info("Shutdown product-service")


app = FastAPI(lifespan=lifespan, title="Product Service")

app.include_router(product_router)
