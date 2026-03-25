from datetime import datetime
from pytest import fixture

from models.customer import Customer


@fixture(name="customer")
def fixture_customer() -> Customer:
    return Customer(
        id="01JFTE35ZRRZWCSKK6TBB1DZCT",
        name="Etevaldo Beltrao Mororo",
        email="etevaldo@gmail.com",
        active=True,
        created_at=datetime(2024, 12, 23, 15, 57, 25, 496623),
        updated_at=None,
    )
