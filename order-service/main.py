import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from clients.studies_llm_client import StudiesLlmClient
from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from clients.weather_client import WeatherClient
from configs.db_conn import get_database_connection
from configs.cache_conn import get_cache_connection
from routes.interaction_router import router as interaction_router
from routes.chat_studies_router import router as chat_studies_router
from routes.order_router import router as order_router
from routes.file_router import router as file_router
from services.chat_studies_service import ChatStudiesService
from services.order_service import OrderService
from services.interaction_service import InteractionService
from services.file_service import FileService
from services.intation_service import IntationService
from services.product_service import ProductService
from services.weather_service import WeatherService
from services.cache_service import CacheService
from storage.order_storage import OrderStorage
from storage.cache_storage import CacheStorage
from storage.question_storage import QuestionStorage
from tools.purchase_tool import PurchaseTool


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    cache_connection = get_cache_connection()

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

    # file
    question_storage = QuestionStorage(db_connection)
    file_service = FileService(question_storage=question_storage)

    # cache
    cache_storage = CacheStorage(cache_connection=cache_connection)
    cache_service = CacheService(cache_storage=cache_storage)

    # tools
    purchase_tool = PurchaseTool(order_service=order_service)

    # llm
    llm_ollama = ChatOllama(
        model="llama3",
        temperature=0.0,
        base_url=os.getenv("OLLAMA_BASE_URL"),
    )

    llm_groq = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.7)

    llm_client = LlmClient(
        llm_ollama=llm_ollama, llm_groq=llm_groq, purchase_tool=purchase_tool
    )
    intation_service = IntationService(llm_client=llm_client)

    # interaction
    interaction_service = InteractionService(
        intation_service=intation_service,
        order_service=order_service,
        product_service=product_service,
        weather_service=weather_service,
        cache_service=cache_service,
        question_storage=question_storage,
    )

    # studies
    studies_llm_client = StudiesLlmClient(llm_ollama=llm_ollama, llm_groq=llm_groq)
    chat_studies_service = ChatStudiesService(llm_client=studies_llm_client)

    yield {
        "order_service": order_service,
        "interaction_service": interaction_service,
        "chat_studies_service": chat_studies_service,
        "file_service": file_service,
    }
    logger.info("Shutdown order-service")


app = FastAPI(lifespan=lifespan, title="Order Service")

app.include_router(order_router)
app.include_router(interaction_router)
app.include_router(chat_studies_router)
app.include_router(file_router)
