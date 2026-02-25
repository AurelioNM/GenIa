import logging
from typing import List

from clients.llm_client import LlmClient
from models.order_request import OrderRequest, ProductRequest
from models.interaction import InteractionOutput, InteractionRequest, IntationEnum
from services.intation_service import IntationService
from services.order_service import OrderService


class InteractionService:
    def __init__(self, intation_service: IntationService, order_service: OrderService):
        self.logger = logging.getLogger(__name__)
        self.intation_service = intation_service
        self.order_service = order_service

    def get_chat_interaction(
        self, interaction_request: InteractionRequest
    ) -> InteractionOutput:
        self.logger.info("Getting chat interaction")

        output: InteractionOutput = self.intation_service.get_intation(
            interaction_request.input
        )

        if output.intation == IntationEnum.PURCHASE_PRODUCT and output.products != None:
            self.logger.info("Start flow on intation PURCHASE_PRODUCT")

            order_request = OrderRequest(
                customer_email=interaction_request.customer_email,
                products=output.products,
            )
            self.order_service.create_order(order_request)

        if output.intation == IntationEnum.UNKNOWN:
            self.logger.info("Start flow on intation UNKNOWN")
            output.output = "I didn't understand the request. Can you be more specific?"

        return output
