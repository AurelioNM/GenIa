import logging
from typing import List

from models.product import ProductList, ProductSummary
from clients.product_client import ProductClient


class ProductService:
    def __init__(
        self,
        product_client: ProductClient,
    ):
        self.logger = logging.getLogger(__name__)
        self.product_client = product_client

    def get_products_by_category(self, product_category: str) -> List[ProductSummary]:
        self.logger.info(f"Getting products: category={product_category}")

        products_list: ProductList = self.product_client.get_products_by_category(
            product_category
        )

        products_summary: List[ProductSummary] = []
        for product in products_list.products:
            products_summary.append(
                ProductSummary(
                    name=product.name,
                    description=product.description,
                    price=product.price,
                )
            )

        return products_summary
