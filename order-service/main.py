import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from configs.db_conn import get_database_connection
from routes.chat_interaction_router import router as chat_interaction_router
from routes.order_router import router as order_router
from services.chat_interaction_service import ChatInteractionService
from services.order_service import OrderService
from storage.order_storage import OrderStorage


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    # order
    order_storage = OrderStorage(db_connection)
    customer_client = CustomerClient(httpx)
    product_client = ProductClient(httpx)
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
    chat_interaction_service = ChatInteractionService(llm_client=llm_client)

    yield {
        "order_service": order_service,
        "chat_interaction_service": chat_interaction_service,
    }
    logger.info("Shutdown order-service")


app = FastAPI(lifespan=lifespan, title="Order Service")

app.include_router(order_router)
app.include_router(chat_interaction_router)
