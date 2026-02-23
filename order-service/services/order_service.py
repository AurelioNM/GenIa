import logging

from models.order_request import OrderRequest, OrderResponse


class OrderService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_order(self, order_request: OrderRequest) -> OrderResponse:
        self.logger.info("Creating order")
        return OrderResponse(id="fake-id")
