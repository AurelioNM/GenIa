import logging
from typing import List
from psycopg2 import DatabaseError
from psycopg2._psycopg import connection

from models.customer import Customer


class CustomerStorage:
    def __init__(self, db_connection: connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    def get_all_customers(self) -> List[Customer]:
        self.logger.info("Searching all customers in DB")
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT id, name, email, active, created_at, updated_at
                    FROM customers
                    WHERE active = True
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()
                customer_list = []

                for row in rows:
                    customer = self.map_customer_row_to_model(row)
                    customer_list.append(customer)

                return customer_list
        except DatabaseError as ex:
            self.logger.error(
                f"Failed to search all customers in DB. DatabaseError: {ex}"
            )
            raise

    def get_customer_by_id(self, id: str) -> Customer:
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT id, name, email, active, created_at, updated_at
                    FROM customers
                    WHERE id = %s
                """

                cursor.execute(sql_query, (id,))
                result = cursor.fetchone()

                if result is None:
                    raise ValueError(f"Customer not found with id={id}")

                return self.map_customer_row_to_model(result)
        except DatabaseError as ex:
            self.logger.error(
                f"Failed to search customer with id={id} in DB. DatabaseError: {ex}"
            )
            raise

    def get_customer_by_email(self, email: str) -> Customer:
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT id, name, email, active, created_at, updated_at
                    FROM customers
                    WHERE email = %s
                """

                cursor.execute(sql_query, (email,))
                result = cursor.fetchone()

                if result is None:
                    raise ValueError(f"Customer not found with email={email}")

                return self.map_customer_row_to_model(result)
        except DatabaseError as ex:
            self.logger.error(
                f"Failed to search customer with email={email} in DB. DatabaseError: {ex}"
            )
            raise

    def create_customer(self, customer: Customer) -> Customer:
        self.logger.info("Inserting customer in DB")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers
                    (id, name, email, active, created_at)
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

                self.db.commit()
                return customer
        except DatabaseError as ex:
            self.logger.error(f"Failed to insert customer in DB. DatabaseError: {ex}")
            self.db.rollback()
            raise

    def map_customer_row_to_model(self, row: List) -> Customer:
        return Customer(
            id=row[0],
            name=row[1],
            email=row[2],
            active=row[3],
            created_at=row[4],
            updated_at=row[5],
        )
