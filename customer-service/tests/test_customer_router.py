from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastmcp import client
from pytest import fixture
import pytest

from main import app
from services.customer_service import CustomerService
from routes.customer_router import get_customer_service


@fixture(name="service")
def fixture_service():
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    app.dependency_overrides[get_customer_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="customer_json")
def fixture_customer_json():
    return {
        "id": "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "name": "Etevaldo Beltrao Mororo",
        "email": "etevaldo@gmail.com",
        "active": True,
        "created_at": "2024-12-23T15:57:25.496623",
        "updated_at": None,
    }


@fixture(name="customer_list_json")
def fixture_customer_list_json(customer_json):
    return [customer_json]


def test_create_customer(service, client, customer, customer_json):
    service.create_customer.return_value = customer

    response = client.post("/v1/customers", json=customer_json)

    assert response.status_code == 201
    assert response.json() == customer_json

    service.create_customer.assert_called_once_with(customer)


def test_create_customer_bad_request(service, client, customer, customer_json):
    service.create_customer.side_effect = ValueError("Customer validation")

    response = client.post("/v1/customers", json=customer_json)

    assert response.status_code == 400
    assert response.json() == {"detail": "Error: Customer validation"}

    service.create_customer.assert_called_once_with(customer)


def test_get_all_customers(service, client, customer, customer_list_json):
    service.get_all_customers.return_value = [customer]

    response = client.get("/v1/customers")

    assert response.status_code == 200
    assert response.json() == customer_list_json

    service.get_all_customers.assert_called_once()


def test_get_all_customers_internal_error(service, client):
    service.get_all_customers.side_effect = Exception("Database error")

    response = client.get("/v1/customers")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error: Database error"}

    service.get_all_customers.assert_called_once()


def test_get_customer_by_id(service, client, customer, customer_json):
    service.get_customer_by_id.return_value = customer

    response = client.get("/v1/customers/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 200
    assert response.json() == customer_json

    service.get_customer_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_get_customer_by_id_not_found(service, client):
    service.get_customer_by_id.side_effect = ValueError("Customer not found")

    response = client.get("/v1/customers/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 404
    assert response.json() == {"detail": "Error: Customer not found"}

    service.get_customer_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_get_customer_by_email(service, client, customer, customer_json):
    service.get_customer_by_email.return_value = customer

    response = client.get("/v1/customers/email/etevaldo@gmail.com")

    assert response.status_code == 200
    assert response.json() == customer_json

    service.get_customer_by_email.assert_called_once_with("etevaldo@gmail.com")


def test_get_customer_by_email_not_found(service, client):
    service.get_customer_by_email.side_effect = ValueError("Customer not found")

    response = client.get("/v1/customers/email/etevaldo@gmail.com")

    assert response.status_code == 404
    assert response.json() == {"detail": "Error: Customer not found"}

    service.get_customer_by_email.assert_called_once_with("etevaldo@gmail.com")
