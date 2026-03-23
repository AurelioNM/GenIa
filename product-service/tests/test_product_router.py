from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from routes.product_router import get_product_service


@fixture(name="service")
def fixture_service():
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    app.dependency_overrides[get_product_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="product_json")
def fixture_product_json():
    return {
        "id": "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "name": "Cat Bed",
        "description": "Bed for cats",
        "price": 20.0,
        "category": "PETS",
        "active": True,
        "created_at": "2024-12-23T15:57:25.496623",
        "updated_at": None,
    }


@fixture(name="product_list_json")
def fixture_product_list_json(product_json):
    return {"products": [product_json]}


@fixture(name="categories_json")
def fixture_categories_json(categories):
    return {"categories": categories.categories}


def test_get_all_products(service, client, product, product_json):
    service.get_all_products.return_value = [product]

    response = client.get("/v1/products")

    assert response.status_code == 200
    assert response.json() == [product_json]

    service.get_all_products.assert_called_once()


def test_get_product_by_id(service, client, product, product_json):
    service.get_product_by_id.return_value = product

    response = client.get("/v1/products/id/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 200
    assert response.json() == product_json

    service.get_product_by_id.assert_called_once()


def test_get_product_by_id_not_found(service, client):
    service.get_product_by_id.side_effect = ValueError("Product not found")

    response = client.get("/v1/products/id/01JFTE35ZRRZWCSKK6TBB1DZCT")

    assert response.status_code == 404

    service.get_product_by_id.assert_called_once_with("01JFTE35ZRRZWCSKK6TBB1DZCT")


def test_get_products_by_names(service, client, product_list, product_list_json):
    service.get_products_by_names.return_value = product_list

    body = {"names": ["Cat Bed"]}
    response = client.post("/v1/products/name", json=body)

    assert response.status_code == 200
    assert response.json() == product_list_json

    service.get_products_by_names.assert_called_once()


def test_get_products_by_names_internal_error(service, client):
    service.get_products_by_names.side_effect = ValueError("Error")

    body = {"names": ["Cat Bed"]}
    response = client.post("/v1/products/name", json=body)

    assert response.status_code == 500

    service.get_products_by_names.assert_called_once()


def test_get_products_by_category(service, client, product_list, product_list_json):
    service.get_products_by_category.return_value = product_list

    response = client.get("v1/products/categories/PETS")

    assert response.status_code == 200
    assert response.json() == product_list_json

    service.get_products_by_category.assert_called_once()


def test_get_products_by_category_internal_error(service, client):
    service.get_products_by_category.side_effect = ValueError("Error")

    response = client.get("v1/products/categories/PETS")

    assert response.status_code == 500

    service.get_products_by_category.assert_called_once()


def test_get_product_categories(service, client, categories, categories_json):
    service.get_product_categories.return_value = categories

    response = client.get("v1/products/categories")

    assert response.status_code == 200
    assert response.json() == categories_json

    service.get_product_categories.assert_called_once()


def test_get_product_categories_internal_error(service, client):
    service.get_product_categories.side_effect = ValueError("Error")

    response = client.get("v1/products/categories")

    assert response.status_code == 500

    service.get_product_categories.assert_called_once()


def test_create_product(service, client, product, product_json):
    service.create_product.return_value = product

    response = client.post("/v1/products", json=product_json)

    assert response.status_code == 201
    assert response.json() == product_json

    service.create_product.assert_called_once_with(product)


def test_create_product_bad_request(service, client, product, product_json):
    service.create_product.side_effect = ValueError("Product validation")

    response = client.post("/v1/products", json=product_json)

    assert response.status_code == 400

    service.create_product.assert_called_once_with(product)
