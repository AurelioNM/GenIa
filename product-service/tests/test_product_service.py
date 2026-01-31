
from unittest.mock import MagicMock
from pytest import fixture
import pytest

from services.product_service import ProductService


@fixture(name="storage")
def fixture_storage():
    return MagicMock()

@fixture(name="service")
def fixture_service(storage):
    return ProductService(storage)

def test_get_all_products(service, storage, product):
    storage.get_all_products.return_value = [product]

    result = service.get_all_products()
    assert result == [product]

    storage.get_all_products.assert_called_once()

def test_get_product_by_id(service, storage, product):
    id = "01JFTE35ZRRZWCSKK6TBB1DZCT"
    
    storage.get_product_by_id.return_value = product

    result = service.get_product_by_id(id)
    assert result == product

    storage.get_product_by_id.assert_called_once_with(id)


def test_create_product(service, storage, product):
    storage.create_product.return_value = product

    result = service.create_product(product)
    assert result == product

    storage.create_product.assert_called_once()

def test_create_product_validation_error(service, storage, product):
    product.price = 0.99

    with pytest.raises(ValueError):
        service.create_product(product)

    storage.create_product.assert_not_called()
