from datetime import datetime
from pytest import fixture

from models.product import Product


@fixture(name="product")
def fixture_product():
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

