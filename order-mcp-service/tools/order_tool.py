import logging

from models.order_request import OrderRequest, OrderResponse
from models.order import MostPurchasedCategory
from services.order_service import OrderService
from fastmcp.exceptions import ToolError


class OrderTool:
    def __init__(
        self,
        order_service: OrderService,
    ):
        self.logger = logging.getLogger(__name__)
        self.order_service = order_service

    def create_order(self, order_request: OrderRequest) -> OrderResponse:
        try:
            self.logger.info(
                f"Started request createOrderV1: body={order_request.model_dump()}"
            )

            response: OrderResponse = self.order_service.create_order(order_request)

            self.logger.info(f"Finished request createOrderV1: response={response}")
            return response
        except Exception as ex:
            self.logger.error(f"Failed request createOrderV1. Error: {ex}")

            raise ToolError(f"Error: {ex}")

    def get_most_purchased_category(self, customer_email: str) -> MostPurchasedCategory:
        try:
            self.logger.info(
                f"Started request getGetMostPurchasedCategoryV1: email={customer_email}"
            )
            category: MostPurchasedCategory = (
                self.order_service.get_most_purchased_category(customer_email)
            )
            response = MostPurchasedCategory(category=category)

            self.logger.info(
                f"Finished request getGetMostPurchasedCategoryV1: response={response}"
            )
            return response
        except Exception as ex:
            self.logger.error(f"Failed request createOrderV1. Error: {ex}")

            raise ToolError(f"Error: {ex}")
