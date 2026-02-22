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


@router.get("/customers", response_model=List[Customer])
def get_all_customers(service: ServiceDep):
    logger.info("Started request getAllCustomers")
    customers_list: List[Customer] = service.get_all_customers()

    logger.info(f"Finished request getAllCustomers: response={customers_list}")
    return customers_list


@router.get("/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str, service: ServiceDep):
    try:
        logger.info(f"Started request getCustomerById: id={id}")
        customer: Customer = service.get_customer_by_id(id)

        logger.info(f"Finished request getCustomerById: response={customer}")
        return customer
    except ValueError as ex:
        logger.error(f"Failed request getCustomerById. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.post("/customers", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: Customer, service: ServiceDep):
    try:
        logger.info(f"Started request createCustomer: body={customer.model_dump()}")
        customer_created: Customer = service.create_customer(customer)

        logger.info(f"Finished request createCustomer: response={customer_created}")
        return customer_created
    except ValueError as ex:
        logger.error(f"Failed request createCustomer. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
