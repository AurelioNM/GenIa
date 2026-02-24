import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.order_request import OrderRequest, OrderResponse
from models.order import OrdersPage
from services.order_service import OrderService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_order_service(request: Request):
    return request.state.order_service


ServiceDep = Annotated[OrderService, Depends(get_order_service)]


@router.get("/v1/orders/customers/email/{customer_email}", response_model=OrdersPage)
def get_orders_by_customer_email(customer_email: str, service: ServiceDep):
    logger.info(f"Started request getOrdersByCustomerEmailV1: email={customer_email}")
    response: OrdersPage = service.get_orders_by_customer_email(customer_email)

    logger.info(f"Finished request getOrdersByCustomerEmailV1: response={response}")
    return response


@router.post(
    "/v1/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponse,
)
def create_order(order_request: OrderRequest, service: ServiceDep):
    try:
        logger.info(f"Started request createOrderV1: body={order_request.model_dump()}")

        response: OrderResponse = service.create_order(order_request)

        logger.info(f"Finished request createOrderV1: response={response}")
        return response
    except ValueError as ex:
        logger.error(f"Failed request createOrderV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
