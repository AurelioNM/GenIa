import logging

from fastapi import HTTPException, status

from models.order_request import OrderRequest, OrderResponse
from models.order import OrdersPage
from services.order_service import OrderService


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
        except ValueError as ex:
            self.logger.error(f"Failed request createOrderV1. Error: {ex}")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
            )

    def get_orders_by_customer_email(self, customer_email: str):
        self.logger.info(
            f"Started request getOrdersByCustomerEmailV1: email={customer_email}"
        )
        response: OrdersPage = self.order_service.get_orders_by_customer_email(
            customer_email
        )

        self.logger.info(
            f"Finished request getOrdersByCustomerEmailV1: response={response}"
        )
        return response
