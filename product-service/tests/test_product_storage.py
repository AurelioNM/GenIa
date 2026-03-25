from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock
from psycopg2 import DatabaseError
from pytest import fixture
import pytest

from storages.product_storage import ProductStorage
from models.product import Product, ProductCategories, ProductNames


@fixture(name="cursor")
def fixture_cursor():
    return MagicMock()


@fixture(name="db_conn")
def fixture_db_conn(cursor):
    db_conn = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor
    return db_conn


@fixture(name="storage")
def fixture_storage(db_conn):
    return ProductStorage(db_conn)


@fixture(name="product_row")
def fixture_product_row():
    return (
        "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "Cat Bed",
        "Bed for cats",
        Decimal("20.0"),
        "PETS",
        True,
        datetime(2024, 12, 23, 15, 57, 25, 496623),
        None,
    )


def test_create_product(cursor, db_conn, storage, product):
    result = storage.create_product(product)
    assert result == product

    db_conn.commit.assert_called_once()

    cursor.execute.assert_called_once_with
    (
        """
        INSERT INTO products (id, name, description, price, category, active, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        (
            product.id,
            product.name,
            product.description,
            product.price,
            product.category,
            product.active,
            product.created_at,
        ),
    )


def test_create_product_database_error(cursor, storage, product, db_conn):
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.create_product(product)

    cursor.execute.assert_called_once()
    db_conn.rollback.assert_called_once()


def test_get_all_products(cursor, storage, product, product_row):
    cursor.fetchall.return_value = [product_row]

    result = storage.get_all_products()
    assert result == [product]

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE active = True
        """
    )


def test_get_all_products_database_error(cursor, storage):
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_all_products()

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_not_called()


def test_get_product_by_id(cursor, storage, product, product_row):
    id = "01JFTE35ZRRZWCSKK6TBB1DZCT"

    cursor.fetchone.return_value = product_row

    result = storage.get_product_by_id(id)
    assert result == product

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE active = %s
        """,
        (id,),
    )


def test_get_product_by_id_value_error(cursor, storage, product, product_row):
    id = "01JFTE35ZRRZWCSKK6TBB1DZCT"

    cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.get_product_by_id(id)

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE active = %s
        """,
        (id,),
    )


def test_get_product_by_id_database_error(cursor, storage, product, product_row):
    id = "01JFTE35ZRRZWCSKK6TBB1DZCT"

    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_product_by_id(id)

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE active = %s
        """,
        (id,),
    )


def test_get_products_by_names(cursor, storage, product, product_row):
    names = ProductNames(names=["Cat Bed"])

    cursor.fetchall.return_value = [product_row]

    result = storage.get_products_by_names(names)
    assert result == [product]

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE name IN (%s)
        """,
        tuple(names),
    )


def test_get_products_by_names_empty_list(cursor, storage, product, product_row):
    names = ProductNames(names=[])

    result = storage.get_products_by_names(names)
    assert result == []

    cursor.fetchall.assert_not_called()
    cursor.execute.assert_not_called()


def test_get_products_by_names_database_error(cursor, storage):
    names = ProductNames(names=["Cat Bed"])

    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_products_by_names(names)

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE name IN (%s)
        """,
        tuple(names),
    )


def test_get_products_by_category(cursor, storage, product, product_row):
    category = "PETS"

    cursor.fetchall.return_value = [product_row]

    result = storage.get_products_by_category(category)
    assert result == [product]

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE category = %s
        """,
        (category,),
    )


def test_get_products_by_category_database_error(cursor, storage):
    category = "PETS"

    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_products_by_category(category)

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, description, price, category, active, created_at, updated_at
            FROM products
            WHERE category = %s
        """,
        (category,),
    )


def test_get_product_categories(cursor, storage, categories):
    cursor.fetchall.return_value = [(category,) for category in categories.categories]

    result = storage.get_product_categories()
    assert result == categories

    cursor.execute.assert_called_once_with
    (
        """
            SELECT DISTINCT category
            FROM products
        """
    )


def test_get_product_categories_database_error(cursor, storage):
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_product_categories()

    cursor.execute.assert_called_once_with
    (
        """
            SELECT DISTINCT category
            FROM products
        """
    )
