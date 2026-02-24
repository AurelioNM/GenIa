import logging
import os
from typing import List
from models.product import Product, ProductList, ProductNames

import httpx


class ProductClient:
    def __init__(self, client_http: httpx):
        self.logger = logging.getLogger(__name__)
        self.client_http = client_http

    def get_products_by_names(self, product_names: ProductNames) -> ProductList:
        try:
            self.logger.info(f"Getting products by names={product_names.names}")

            url = f"{os.getenv('PRODUCT_BASE_URL')}/v1/products/name"

            response = self.client_http.post(url, json=product_names.model_dump())

            response.raise_for_status()

            self.logger.debug(f"Get products response: {response}")

            product = ProductList(**response.json())

            self.logger.debug(f"Mapped response dto: {product}")

            return product
        except httpx.RequestError as e:
            self.logger.error(f"Failed to get products: {e}")
            raise
