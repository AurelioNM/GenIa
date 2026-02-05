import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.product import Product
from services.product_service import ProductService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_product_service(request: Request):
    return request.state.product_service


ServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.get("/products", response_model=List[Product])
def get_all_products(service: ServiceDep):
    logger.info("Started request getAllProducts")
    products_list: List[Product] = service.get_all_products()

    logger.info(f"Finished request getAllProducts: response={products_list}")
    return products_list


@router.get("/products/{id}", response_model=Product)
def get_product_by_id(id: str, service: ServiceDep):
    try:
        logger.info(f"Started request getProductById: id={id}")
        product: Product = service.get_product_by_id(id)

        logger.info(f"Finished request getProductById: response={product}")
        return product
    except ValueError as ex:
        logger.error(f"Failed request getProductById. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_product(product: Product, service: ServiceDep):
    try:
        logger.info(f"Started request createProduct: body={product.model_dump()}")
        product_created: Product = service.create_product(product)

        logger.info(f"Finished request createProduct: response={product_created}")
        return product_created
    except ValueError as ex:
        logger.error(f"Failed request createProduct. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
