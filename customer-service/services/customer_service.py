import logging
from typing import List

from models.customer import Customer
from storages.customer_storage import CustomerStorage


class CustomerService:
    def __init__(self, storage: CustomerStorage):
        self.logger = logging.getLogger(__name__)
        self.storage = storage

    def get_all_customers(self) -> List[Customer]:
        self.logger.info("Getting all customers")
        return self.storage.get_all_customers()

    def get_customer_by_id(self, id: str) -> Customer:
        self.logger.info("Getting customer by id")
        return self.storage.get_customer_by_id(id)

    def create_customer(self, customer: Customer) -> Customer:
        self.logger.info("Creating customer")
        return self.storage.create_customer(customer)
