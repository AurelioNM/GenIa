import logging
from typing import List
from langchain_core.tools import StructuredTool

from services.product_service import ProductService
from services.order_service import OrderService
from models.product import ProductSummary
from models.tool_output import SuggestProductToolOutput
from models.tool_input import SuggestProductOnHistoryToolInput


class SuggestProductOnHistoryTool:
    def __init__(self, order_service: OrderService, product_service: ProductService):
        self.logger = logging.getLogger(__name__)
        self.order_service = order_service
        self.product_service = product_service

    def _execute(
        self,
        email: str,
    ) -> SuggestProductToolOutput:
        self.logger.info(f"Executing tool suggest_product_on_history: email={email}")

        category: str = self.order_service.get_most_purchased_category(email)

        products: List[ProductSummary] = self.product_service.get_products_by_category(
            category
        )

        return SuggestProductToolOutput(products=products).model_dump()

    def get_tool(self):
        return StructuredTool.from_function(
            func=self._execute,
            name="suggest_product_on_history",
            description="Get product list based on a customer's purchase history. Returns a list of products with their names and prices.",
            args_schema=SuggestProductOnHistoryToolInput,
        )
