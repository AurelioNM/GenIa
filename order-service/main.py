import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from configs.db_conn import get_database_connection
from routes.chat_interaction_router import router as chat_interaction_router
from services.chat_interaction_service import ChatInteractionService


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()

    llm = ChatOllama(
        model="llama3",
        temperature=0.0,
        base_url=os.getenv("OLLAMA_BASE_URL"),
        # format="json",  # improves structured reliability
    )
    llm_client = LlmClient(llm=llm)
    chat_interaction_service = ChatInteractionService(llm_client=llm_client)

    yield {
        "chat_interaction_service": chat_interaction_service,
    }
    logger.info("Shutdown order-service")


app = FastAPI(lifespan=lifespan, title="Order Service")

app.include_router(chat_interaction_router)
