import logging

from pymongo import MongoClient, database
from pymongo.errors import PyMongoError

from models.order import Order, OrdersPage


class OrderStorage:
    def __init__(self, db_connection: MongoClient):
        self.logger = logging.getLogger(__name__)
        self.db_connection: MongoClient = db_connection
        self.collection: database.Database = self.db_connection.get_collection("order")

    def create_order(self, order: Order) -> str:
        try:
            self.logger.info(f"Inserting order in DB: {order.model_dump()}")
            result = self.collection.insert_one(order.model_dump())

            return str(result.inserted_id)

        except PyMongoError as e:
            self.logger.error(f"Failed to create order in DB. PyMongoError: {e}")
            raise

    def get_orders_by_customer_email(self, customer_email: str) -> OrdersPage:
        try:
            self.logger.info("Finding orders in DB")
            result = self.collection.find({"customer.email": customer_email})

            orders = [Order(**order) for order in result]

            return OrdersPage(orders=orders)

        except PyMongoError as e:
            self.logger.error(
                f"Failed to find orders in DB by customer id. PyMongoError: {e}"
            )
            raise
