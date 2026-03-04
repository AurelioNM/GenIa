import logging
from typing import List

from models.order_request import OrderRequest
from models.interaction import (
    InteractionOutput,
    InteractionOutputV2,
    InteractionRequest,
    IntationEnum,
)
from models.product import ProductSummary
from models.weather import Weather
from services.intation_service import IntationService
from services.order_service import OrderService
from services.product_service import ProductService
from services.cache_service import CacheService
from services.weather_service import WeatherService
from storage.question_storage import QuestionStorage


class InteractionService:
    def __init__(
        self,
        intation_service: IntationService,
        order_service: OrderService,
        product_service: ProductService,
        weather_service: WeatherService,
        cache_service: CacheService,
        question_storage: QuestionStorage,
    ):
        self.logger = logging.getLogger(__name__)
        self.intation_service = intation_service
        self.order_service = order_service
        self.product_service = product_service
        self.weather_service = weather_service
        self.cache_service = cache_service
        self.question_storage = question_storage

    def get_chat_interaction(
        self, interaction_request: InteractionRequest, session_id: str
    ) -> InteractionOutput:
        self.logger.info("Getting chat interaction")

        history = self.cache_service.get_chat_history(session_id)

        output: InteractionOutput = self.intation_service.get_intation(
            interaction_request, history
        )

        if output.intation == IntationEnum.PURCHASE_PRODUCT and output.products != None:
            self._execute_purchase_flow(interaction_request, output)

        if output.intation == IntationEnum.SUGGEST_PRODUCT_BASED_ON_CATEGORY:
            self._execute_product_suggestion_on_category_flow(output)

        if output.intation == IntationEnum.SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY:
            self._execute_product_suggestion_on_order_history_flow(
                interaction_request, output
            )

        if output.intation == IntationEnum.SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER:
            self._execute_day_suggestion_on_weather_flow(interaction_request, output)

        if output.intation == IntationEnum.TARANTINO_QUESTION:
            self._execute_tarantino_question_flow(interaction_request, output)

        self.cache_service.save_chat_history(
            session_id, history, interaction_request, output
        )

        return output

    async def get_chat_interaction_with_tools(
        self, interaction_request: InteractionRequest, session_id: str
    ) -> InteractionOutputV2:
        self.logger.info("Getting chat interaction")

        history = self.cache_service.get_chat_history(session_id)

        output: InteractionOutputV2 = (
            await self.intation_service.get_intation_with_tools(
                interaction_request, history
            )
        )

        self.cache_service.save_chat_history(
            session_id, history, interaction_request, output
        )

        return output

    def _execute_purchase_flow(
        self, input: InteractionRequest, output: InteractionOutput
    ):
        self.logger.info("Executing flow for intation PURCHASE_PRODUCT")
        order_request = OrderRequest(
            customer_email=input.customer_email,
            products=output.products,
        )
        self.order_service.create_order(order_request)

    def _execute_product_suggestion_on_category_flow(self, output: InteractionOutput):
        self.logger.info(
            "Executing flow for intation SUGGEST_PRODUCT_BASED_ON_CATEGORY"
        )
        products: List[ProductSummary] = self.product_service.get_products_by_category(
            output.category
        )

        product_lines = "\n".join(
            f"- {product.name}: ${product.price:.2f}" for product in products
        )

        output.output = f"""Here are some great options based on the category {output.category}:

        {product_lines}

        Let me know if you'd like to purchase any of them!"""

    def _execute_product_suggestion_on_order_history_flow(
        self, input: InteractionRequest, output: InteractionOutput
    ):
        self.logger.info(
            "Executing flow for intation SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY"
        )
        category: str = self.order_service.get_most_purchased_category(
            input.customer_email
        )

        products: List[ProductSummary] = self.product_service.get_products_by_category(
            category
        )

        product_lines = "\n".join(
            f"- {product.name}: ${product.price:.2f}" for product in products
        )

        output.category = category
        output.output = f"""Here are some great options based on your \
        most purchased category {category}:

        {product_lines}

        Let me know if you'd like to purchase any of them!"""

    def _execute_day_suggestion_on_weather_flow(
        self, input: InteractionRequest, output: InteractionOutput
    ):
        self.logger.info(
            "Executing flow for intation SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER"
        )
        forecast: List[Weather] = self.weather_service.get_weather_forecast()
        products: List[ProductSummary] = self.product_service.get_products_by_category(
            "WEATHER"
        )

        output.category = "WEATHER"
        output.output = self.intation_service.process_weather_intation(
            input.input, forecast, products
        )

    def _execute_tarantino_question_flow(
        self, input: InteractionRequest, output: InteractionOutput
    ):
        self.logger.info("Executing flow for intation TARANTINO_QUESTION")
        questions = self.question_storage.search_similar_questions(input.input)

        output.output = self.intation_service.process_question_intation(
            input.input, questions
        )
