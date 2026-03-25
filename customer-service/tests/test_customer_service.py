from unittest.mock import MagicMock
from pytest import fixture
import pytest

from services.customer_service import CustomerService


@fixture(name="storage")
def fixture_storage():
    return MagicMock()


@fixture(name="service")
def fixture_service(storage):
    return CustomerService(storage)


def test_create_customer(service, storage, customer):
    storage.create_customer.return_value = customer

    result = service.create_customer(customer)
    assert result == customer

    storage.create_customer.assert_called_once_with(customer)


def test_get_all_customers(service, storage, customer):
    storage.get_all_customers.return_value = [customer]

    result = service.get_all_customers()
    assert result == [customer]

    storage.get_all_customers.assert_called_once()


def test_get_customer_by_id(service, storage, customer):
    id = "01JFTE35ZRRZWCSKK6TBB1DZCT"

    storage.get_customer_by_id.return_value = customer

    result = service.get_customer_by_id(id)
    assert result == customer

    storage.get_customer_by_id.assert_called_once_with(id)


def test_get_customer_by_email(service, storage, customer):
    email = "etevaldo@gmail.com"

    storage.get_customer_by_email.return_value = customer

    result = service.get_customer_by_email(email)
    assert result == customer

    storage.get_customer_by_email.assert_called_once_with(email)
