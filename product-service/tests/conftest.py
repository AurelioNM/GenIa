from datetime import datetime
from typing import List
from pytest import fixture

from models.product import Product, ProductCategories, ProductList


@fixture(name="product")
def fixture_product() -> Product:
    return Product(
        id="01JFTE35ZRRZWCSKK6TBB1DZCT",
        name="Cat Bed",
        description="Bed for cats",
        price=20.0,
        category="PETS",
        active=True,
        created_at=datetime(2024, 12, 23, 15, 57, 25, 496623),
        updated_at=None,
    )


@fixture(name="product_list")
def fixture_product_list(product) -> ProductList:
    return ProductList(products=[product])


@fixture(name="categories")
def fixture_categories() -> ProductCategories:
    return ProductCategories(categories=["DRINK", "SNACKS", "TECH", "PETS", "WEATHER"])
