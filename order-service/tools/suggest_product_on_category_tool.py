import logging
from typing import List
from langchain_core.tools import StructuredTool

from services.product_service import ProductService
from models.product import ProductSummary
from models.tool_output import SuggestProductToolOutput
from models.tool_input import SuggestProductOnCategoryToolInput


class SuggestProductOnCategoryTool:
    def __init__(self, product_service: ProductService):
        self.logger = logging.getLogger(__name__)
        self.product_service = product_service

    def _execute(
        self,
        category: str,  # TODO make it an ENUM
    ) -> SuggestProductToolOutput:
        self.logger.info(
            f"Executing tool suggest_product_on_category: category={category}"
        )

        products: List[ProductSummary] = self.product_service.get_products_by_category(
            category
        )

        return SuggestProductToolOutput(products=products).model_dump()

    def get_tool(self):
        return StructuredTool.from_function(
            func=self._execute,
            name="suggest_product_on_category",
            description="Get product list based on a category the customer chose. Returns a list of products with their names and prices.",
            args_schema=SuggestProductOnCategoryToolInput,
        )
