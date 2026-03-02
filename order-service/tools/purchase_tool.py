import logging

from langchain_core.tools import StructuredTool

from models.interaction import InteractionOutput
from langchain.tools import tool
from services.order_service import OrderService
from models.order_request import OrderRequest


class PurchaseTool:
    def __init__(self, order_service: OrderService):
        self.logger = logging.getLogger(__name__)
        self.order_service = order_service

    def _purchase_product(self, output: InteractionOutput) -> str:
        """
        Creates a purchase order for the given customer with the specified products.
        """

        self.logger.info(
            f"Executing TOOL purchase_product: email={output.customer_email}, products={output.products}"
        )
        order_request = OrderRequest(
            customer_email=output.customer_email,
            products=output.products,
        )
        self.order_service.create_order(order_request)

        self.logger.info(
            f"Successfully executed TOOL purchase_product: email={output.customer_email}, products={output.products}"
        )
        return "Order successfully created."

    def get_tool(self):
        return StructuredTool.from_function(
            func=self._purchase_product,
            name="purchase_product",
            description="Use this tool when the user wants to purchase products.",
            args_schema=InteractionOutput,
        )
