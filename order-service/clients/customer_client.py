import logging
import os
from typing import List
from models.customer import Customer

import httpx


class CustomerClient:
    def __init__(self, client_http: httpx):
        self.logger = logging.getLogger(__name__)
        self.client_http = client_http

    def get_city_forecast(self, customer_email: str) -> Customer:
        try:
            self.logger.info(f"Getting customer by email={customer_email}")

            url = (
                f"{os.getenv('CUSTOMER_BASE_URL')}/v1/customers/email/{customer_email}"
            )

            response = self.client_http.get(url)

            response.raise_for_status()

            self.logger.debug(f"Get customer response: {response}")

            customer = Customer(**response.json())

            self.logger.debug(f"Mapped response dto: {customer}")

            return customer
        except httpx.RequestError as e:
            self.logger.error(f"Failed to get customer: {e}")
            raise
