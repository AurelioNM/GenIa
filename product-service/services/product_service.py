import logging
from typing import List

from models.product import Product, ProductList, ProductNames
from storages.product_storage import ProductStorage


class ProductService:
    def __init__(self, storage: ProductStorage):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        self.MINIMUM_PRICE = 1.0

    def get_all_products(self) -> List[Product]:
        self.logger.info("Getting all products")
        return self.storage.get_all_products()

    def get_product_by_id(self, id: str) -> Product:
        self.logger.info("Getting product by id")
        return self.storage.get_product_by_id(id)

    def get_products_by_names(self, names: ProductNames) -> ProductList:
        self.logger.info("Getting products by names")
        products = self.storage.get_products_by_names(names)

        return ProductList(products=products)

    def get_products_by_category(self, category: str) -> ProductList:
        self.logger.info("Getting products by category")
        products = self.storage.get_products_by_category(category)

        return ProductList(products=products)

    def create_product(self, product: Product) -> Product:
        self.logger.info("Creating product")

        self.validate_product(product)

        return self.storage.create_product(product)

    def validate_product(self, product: Product):
        if product.price < self.MINIMUM_PRICE:
            error = ValueError(
                f"Price must be equal or greater than {self.MINIMUM_PRICE}"
            )
            self.logger.error(f"Failed on product validation. Error: {error}")
            raise error
