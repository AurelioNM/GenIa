import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.order_request import OrderRequest, OrderResponse
from services.order_service import OrderService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_order_service(request: Request):
    return request.state.order_service


ServiceDep = Annotated[OrderService, Depends(get_order_service)]


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
