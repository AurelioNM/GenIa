import logging
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import httpx
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from clients.llm_client import LlmClient
from clients.studies_llm_client import StudiesLlmClient
from clients.product_client import ProductClient
from clients.weather_client import WeatherClient
from configs.db_conn import get_database_connection
from configs.cache_conn import get_cache_connection
from configs.model_conn import get_agent_executor
from routes.interaction_router import router as interaction_router
from routes.chat_studies_router import router as chat_studies_router
from routes.file_router import router as file_router
from services.chat_studies_service import ChatStudiesService
from services.interaction_service import InteractionService
from services.file_service import FileService
from services.intation_service import IntationService
from services.product_service import ProductService
from services.weather_service import WeatherService
from services.cache_service import CacheService
from storage.cache_storage import CacheStorage
from storage.question_storage import QuestionStorage
from tools.suggest_product_on_category_tool import SuggestProductOnCategoryTool
from tools.answer_question_tool import GetQuestionAnswerBaseTool
from tools.suggest_day_and_product_on_weather import SuggestDayAndProductOnWeatherTool


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    cache_connection = get_cache_connection()

    # product
    product_client = ProductClient(httpx)
    product_service = ProductService(product_client=product_client)

    # weather
    weather_client = WeatherClient(httpx)
    weather_service = WeatherService(weather_client=weather_client)

    # file
    question_storage = QuestionStorage(db_connection)
    file_service = FileService(question_storage=question_storage)

    # cache
    cache_storage = CacheStorage(cache_connection=cache_connection)
    cache_service = CacheService(cache_storage=cache_storage)

    # tools
    suggest_product_on_category_tool = SuggestProductOnCategoryTool(
        product_service=product_service
    )
    suggest_day_and_product_on_weather_tool = SuggestDayAndProductOnWeatherTool(
        weather_service=weather_service, product_service=product_service
    )
    get_question_answer_base_tool = GetQuestionAnswerBaseTool(
        question_storage=question_storage
    )

    # llm
    llm_ollama = ChatOllama(
        model="llama3",
        temperature=0.0,
        base_url=os.getenv("OLLAMA_BASE_URL"),
    )

    llm_groq = ChatGroq(model_name="openai/gpt-oss-120b", temperature=0.7)

    agent_executor = await get_agent_executor(
        llm_groq=llm_groq,
        suggest_product_on_category_tool=suggest_product_on_category_tool,
        suggest_day_and_product_on_weather_tool=suggest_day_and_product_on_weather_tool,
        get_question_answer_base_tool=get_question_answer_base_tool,
    )

    llm_client = LlmClient(
        default_model=llm_groq,
        agent_executor=agent_executor,
    )
    intation_service = IntationService(llm_client=llm_client)

    # interaction
    interaction_service = InteractionService(
        intation_service=intation_service,
        cache_service=cache_service,
    )

    # studies
    studies_llm_client = StudiesLlmClient(llm_ollama=llm_ollama, llm_groq=llm_groq)
    chat_studies_service = ChatStudiesService(llm_client=studies_llm_client)

    yield {
        "interaction_service": interaction_service,
        "chat_studies_service": chat_studies_service,
        "file_service": file_service,
    }
    logger.info("Shutdown order-service")


app = FastAPI(lifespan=lifespan, title="Chat Agent Service")

app.include_router(interaction_router)
app.include_router(chat_studies_router)
app.include_router(file_router)
