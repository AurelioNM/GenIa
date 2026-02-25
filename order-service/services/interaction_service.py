import logging
from typing import List

from models.order_request import OrderRequest
from models.interaction import InteractionOutput, InteractionRequest, IntationEnum
from models.product import ProductSummary
from services.intation_service import IntationService
from services.order_service import OrderService
from services.product_service import ProductService


class InteractionService:
    def __init__(
        self,
        intation_service: IntationService,
        order_service: OrderService,
        product_service: ProductService,
    ):
        self.logger = logging.getLogger(__name__)
        self.intation_service = intation_service
        self.order_service = order_service
        self.product_service = product_service

    def get_chat_interaction(
        self, interaction_request: InteractionRequest
    ) -> InteractionOutput:
        self.logger.info("Getting chat interaction")

        # TODO IA needs to give me the category
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

        if output.intation == IntationEnum.SUGGEST_PRODUCT_BASED_ON_CATEGORY:
            self.logger.info("Start flow on intation SUGGEST_PRODUCT_BASED_ON_CATEGORY")
            products: List[ProductSummary] = (
                self.product_service.get_products_by_category(output.category)
            )

            product_lines = "\n".join(
                f"- {product.name}: ${product.price:.2f}" for product in products
            )

            output.output = f"""
            Here are some great options based on the category {output.category}:
            
            {product_lines}

            Let me know if you'd like to purchase any of them!
            """

        if output.intation == IntationEnum.UNKNOWN:
            self.logger.info("Start flow on intation UNKNOWN")
            output.output = "I didn't understand the request. Can you be more specific?"

        return output
