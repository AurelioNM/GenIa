import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from configs.db_conn import get_database_connection
from routes.customer_router import router as customer_router
from services.customer_service import CustomerService

from storages.customer_storage import CustomerStorage


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    customer_storage = CustomerStorage(db_connection=db_connection)
    customer_service = CustomerService(customer_storage)

    yield {
        "customer_service": customer_service,
    }
    logger.info("Shutdown customer-service")


app = FastAPI(lifespan=lifespan, title="Customer Service")

app.include_router(customer_router)
