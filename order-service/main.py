import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from clients.weather_client import WeatherClient
from configs.db_conn import get_database_connection
from routes.interaction_router import router as interaction_router
from routes.chat_studies_router import router as chat_studies_router
from routes.order_router import router as order_router
from services.chat_studies_service import ChatStudiesService
from services.order_service import OrderService
from services.interaction_service import InteractionService
from services.intation_service import IntationService
from services.product_service import ProductService
from services.weather_service import WeatherService
from storage.order_storage import OrderStorage


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    # product
    product_client = ProductClient(httpx)
    product_service = ProductService(product_client=product_client)

    # customer
    customer_client = CustomerClient(httpx)

    # weather
    weather_client = WeatherClient(httpx)
    weather_service = WeatherService(weather_client=weather_client)

    # order
    order_storage = OrderStorage(db_connection)
    order_service = OrderService(
        order_storage=order_storage,
        customer_client=customer_client,
        product_client=product_client,
    )

    # llm
    llm = ChatOllama(
        model="llama3",
        temperature=0.0,
        base_url=os.getenv("OLLAMA_BASE_URL"),
        # format="json",  # improves structured reliability
    )
    llm_client = LlmClient(llm=llm)
    intation_service = IntationService(llm_client=llm_client)

    # interaction
    interaction_service = InteractionService(
        intation_service=intation_service,
        order_service=order_service,
        product_service=product_service,
        weather_service=weather_service,
    )

    # studies
    chat_studies_service = ChatStudiesService(llm_client=llm_client)

    yield {
        "order_service": order_service,
        "interaction_service": interaction_service,
        "chat_studies_service": chat_studies_service,
    }
    logger.info("Shutdown order-service")


app = FastAPI(lifespan=lifespan, title="Order Service")

app.include_router(order_router)
app.include_router(interaction_router)
app.include_router(chat_studies_router)
