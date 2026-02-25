import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.product import Product, ProductList, ProductNames
from services.product_service import ProductService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_product_service(request: Request):
    return request.state.product_service


ServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.get("/v1/products", response_model=List[Product])
def get_all_products(service: ServiceDep):
    logger.info("Started request getAllProductsV1")
    products_list: List[Product] = service.get_all_products()

    logger.info(f"Finished request getAllProductsV1: response={products_list}")
    return products_list


@router.get("/v1/products/{id}", response_model=Product)
def get_product_by_id(id: str, service: ServiceDep):
    try:
        logger.info(f"Started request getProductByIdV1: id={id}")
        product: Product = service.get_product_by_id(id)

        logger.info(f"Finished request getProductByIdV1: response={product}")
        return product
    except ValueError as ex:
        logger.error(f"Failed request getProductByIdV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.post("/v1/products/name", response_model=ProductList)
def get_products_by_names(names: ProductNames, service: ServiceDep):
    try:
        logger.info(f"Started request getProductsByNamesV1: names={names.model_dump()}")
        products: ProductList = service.get_products_by_names(names)

        logger.info(f"Finished request getProductsByNamesV1: response={products}")
        return products
    except ValueError as ex:
        logger.error(f"Failed request getProductsByNamesV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.get("/v1/products/category/{category}", response_model=ProductList)
def get_products_by_category(category: str, service: ServiceDep):
    try:
        logger.info(f"Started request getProductByCategoryV1: category={category}")
        product: ProductList = service.get_products_by_category(category)

        logger.info(f"Finished request getProductByCategoryV1: response={product}")
        return product
    except ValueError as ex:
        logger.error(f"Failed request getProductByCategoryV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.post(
    "/v1/products", status_code=status.HTTP_201_CREATED, response_model=Product
)
def create_product(product: Product, service: ServiceDep):
    try:
        logger.info(f"Started request createProductV1: body={product.model_dump()}")
        product_created: Product = service.create_product(product)

        logger.info(f"Finished request createProductV1: response={product_created}")
        return product_created
    except ValueError as ex:
        logger.error(f"Failed request createProductV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
