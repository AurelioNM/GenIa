from collections import defaultdict
import logging
from typing import List

from models.customer import Customer
from models.order import Order, OrdersPage
from models.order_request import OrderRequest, OrderResponse
from models.product import Product, ProductList, ProductNames
from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from storage.order_storage import OrderStorage


class OrderService:
    def __init__(
        self,
        order_storage: OrderStorage,
        customer_client: CustomerClient,
        product_client: ProductClient,
    ):
        self.logger = logging.getLogger(__name__)
        self.order_storage = order_storage
        self.customer_client = customer_client
        self.product_client = product_client

    def get_orders_by_customer_email(self, customer_email: str) -> OrdersPage:
        self.logger.info("Getting orders by customer email...")
        return self.order_storage.get_orders_by_customer_email(customer_email)

    def get_most_purchased_category(self, customer_email: str) -> str:
        self.logger.info("Getting most purchased category")
        orders_page: OrdersPage = self.order_storage.get_orders_by_customer_email(
            customer_email
        )

        category_counter = defaultdict(int)

        for order in orders_page.orders:
            for product in order.products:
                quantity = product.quantity if product.quantity is not None else 1
                category_counter[product.category] += quantity

        self.logger.info(f"Category quantity dict: {category_counter}")

        # Return the category with most sum of quantity
        category = max(category_counter, key=category_counter.get)

        self.logger.info(f"Most purchased category: {category}")
        return category

    def create_order(self, order_request: OrderRequest) -> OrderResponse:
        self.logger.info(f"Creating order: {order_request}")

        customer: Customer = self.customer_client.get_customer_by_email(
            order_request.customer_email
        )

        product_names = [product.name for product in order_request.products]
        products_list: ProductList = self.product_client.get_products_by_names(
            ProductNames(names=product_names)
        )

        # TODO this only is necessary for the llm intention flow
        # maybe move to a previous step
        self._update_products_quantity(order_request, products_list)

        total_value = self._get_total_value(products_list.products)
        order = Order(
            customer=customer,
            products=products_list.products,
            total_value=total_value,
        )

        id = self.order_storage.create_order(order)
        return OrderResponse(id=id, total_value=total_value)

    # TODO move these private functions to the models
    def _update_products_quantity(
        self, order_request: OrderRequest, products_list: ProductList
    ):
        # Build a lookup dict: { name -> quantity }
        quantity_map = {
            product.name: product.quantity for product in order_request.products
        }

        # Inject quantity into products
        for product in products_list.products:
            product.quantity = quantity_map.get(product.name)

        self.logger.info(f"Updated products: {products_list}")

    def _get_total_value(self, products: List[Product]) -> float:
        total = 0.0

        for product in products:
            if product.quantity is None:
                raise ValueError(f"Product '{product.name}' has no quantity defined.")

            total += product.price * product.quantity

        self.logger.info(f"Order total value: {total}")
        return total
