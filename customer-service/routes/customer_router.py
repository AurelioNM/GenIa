import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.customer import Customer
from services.customer_service import CustomerService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_customer_service(request: Request):
    return request.state.customer_service


ServiceDep = Annotated[CustomerService, Depends(get_customer_service)]


@router.get("/v1/customers", response_model=List[Customer])
def get_all_customers(service: ServiceDep):
    logger.info("Started request getAllCustomersV1")
    customers_list: List[Customer] = service.get_all_customers()

    logger.info(f"Finished request getAllCustomersV1: response={customers_list}")
    return customers_list


@router.get("/v1/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str, service: ServiceDep):
    try:
        logger.info(f"Started request getCustomerByIdV1: id={id}")
        customer: Customer = service.get_customer_by_id(id)

        logger.info(f"Finished request getCustomerByIdV1: response={customer}")
        return customer
    except ValueError as ex:
        logger.error(f"Failed request getCustomerByIdV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.get("/v1/customers/email/{email}", response_model=Customer)
def get_customer_by_email(email: str, service: ServiceDep):
    try:
        logger.info(f"Started request getCustomerByEmailV1: email={email}")
        customer: Customer = service.get_customer_by_email(email)

        logger.info(f"Finished request getCustomerByEmailV1: response={customer}")
        return customer
    except ValueError as ex:
        logger.error(f"Failed request getCustomerByEmailV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.post(
    "/v1/customers", status_code=status.HTTP_201_CREATED, response_model=Customer
)
def create_customer(customer: Customer, service: ServiceDep):
    try:
        logger.info(f"Started request createCustomerV1: body={customer.model_dump()}")
        customer_created: Customer = service.create_customer(customer)

        logger.info(f"Finished request createCustomerV1: response={customer_created}")
        return customer_created
    except ValueError as ex:
        logger.error(f"Failed request createCustomerV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
