import logging
from typing import List
from langchain_core.tools import StructuredTool

from services.order_service import OrderService
from models.order_request import OrderRequest, ProductRequest
from models.tool_input import PurchaseProductToolInput


class ProcessPurchaseTool:
    def __init__(self, order_service: OrderService):
        self.logger = logging.getLogger(__name__)
        self.order_service = order_service

    def _execute(
        self,
        email: str,
        products: List[ProductRequest],
    ) -> dict[str, str]:
        try:
            self.logger.info(
                f"Executing tool purchase_product: email={email}, products={products}"
            )

            order_request = OrderRequest(
                customer_email=email,
                products=products,
            )
            self.order_service.create_order(order_request)

            self.logger.info(
                f"Successfully executed tool purchase_product: email={email}, products={products}"
            )
            return {"status": "success"}

        except Exception as e:
            self.logger.error(f"Error executing tool purchase_product: {e}")
            return {"status": "error"}

    def get_tool(self):
        return StructuredTool.from_function(
            func=self._execute,
            name="purchase_product",
            description="""Creates a purchase order for the given customer with the specified products and quantities.

            Args:
                customer_email: The email of the customer making the purchase.
                products: A list of products to purchase.

            Returns:
                A dictionary containing the status of the purchase.
            """,
            args_schema=PurchaseProductToolInput,
        )
