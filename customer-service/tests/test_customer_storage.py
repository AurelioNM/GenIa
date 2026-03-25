from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock
from psycopg2 import DatabaseError
from pytest import fixture
import pytest

from storages.customer_storage import CustomerStorage
from models.customer import Customer


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
    return CustomerStorage(db_conn)


@fixture(name="customer_row")
def fixture_customer_row():
    return (
        "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "Etevaldo Beltrao Mororo",
        "etevaldo@gmail.com",
        True,
        datetime(2024, 12, 23, 15, 57, 25, 496623),
        None,
    )


def test_create_customer(cursor, db_conn, storage, customer):
    result = storage.create_customer(customer)
    assert result == customer

    db_conn.commit.assert_called_once()

    cursor.execute.assert_called_once_with
    (
        """
        INSERT INTO customers (id, name, email, active, created_at)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (
            customer.id,
            customer.name,
            customer.email,
            customer.active,
            customer.created_at,
        ),
    )


def test_create_customer_database_error(cursor, db_conn, storage, customer):
    db_conn.cursor.return_value.__enter__.side_effect = DatabaseError("DB error")

    with pytest.raises(DatabaseError):
        storage.create_customer(customer)

    db_conn.cursor.execute.assert_not_called()
    db_conn.rollback.assert_called_once()


def get_all_customers(cursor, storage, customer, customer_row):
    cursor.fetchall.return_value = [customer_row]

    result = storage.get_all_customers()
    assert result == [customer]

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE active = True
        """
    )


def test_get_all_customers_database_error(cursor, storage):
    cursor.execute.side_effect = DatabaseError("DB error")

    with pytest.raises(DatabaseError):
        storage.get_all_customers()

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_not_called()


def test_get_customer_by_id(cursor, storage, customer, customer_row):
    cursor.fetchone.return_value = customer_row

    result = storage.get_customer_by_id(customer.id)
    assert result == customer

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE id = %s
        """,
        (customer.id,),
    )


def test_get_customer_by_id_not_found(cursor, storage):
    cursor.fetchone.return_value = None

    with pytest.raises(ValueError) as exc_info:
        storage.get_customer_by_id("nonexistent_id")

    assert str(exc_info.value) == "Customer not found with id=nonexistent_id"
    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE id = %s
        """,
        ("nonexistent_id",),
    )


def test_get_customer_by_id_database_error(cursor, storage):
    cursor.execute.side_effect = DatabaseError("DB error")

    with pytest.raises(DatabaseError):
        storage.get_customer_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE id = %s
        """,
        ("01JFTE35ZRRZWCSKK6TBB1DZCT",),
    )


def test_get_customer_by_email(cursor, storage, customer, customer_row):
    cursor.fetchone.return_value = customer_row

    result = storage.get_customer_by_email(customer.email)
    assert result == customer

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE email = %s
        """,
        (customer.email,),
    )


def test_get_customer_by_email_not_found(cursor, storage):
    cursor.fetchone.return_value = None

    with pytest.raises(ValueError) as exc_info:
        storage.get_customer_by_email("nonexistent@gmail.com")

    assert str(exc_info.value) == "Customer not found with email=nonexistent@gmail.com"
    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE email = %s
        """,
        ("nonexistent@gmail.com",),
    )


def test_get_customer_by_email_database_error(cursor, storage):
    cursor.execute.side_effect = DatabaseError("DB error")

    with pytest.raises(DatabaseError):
        storage.get_customer_by_email("nonexistent@gmail.com")

    cursor.execute.assert_called_once_with
    (
        """
            SELECT id, name, email, active, created_at, updated_at
            FROM customers
            WHERE email = %s
        """,
        ("nonexistent@gmail.com",),
    )
