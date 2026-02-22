import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from configs.db_conn import get_database_connection
from routes.product_router import router as product_router
from routes.suggestion_router import router as suggestion_router
from services.product_service import ProductService
from services.suggestion_service import SuggestionService

from storages.product_storage import ProductStorage


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    # Product
    product_storage = ProductStorage(db_connection=db_connection)
    product_service = ProductService(product_storage)

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
        "suggestion_service": suggestion_service,
    }
    logger.info("Shutdown product-service")


app = FastAPI(lifespan=lifespan, title="Product Service")

app.include_router(product_router)
app.include_router(suggestion_router)
