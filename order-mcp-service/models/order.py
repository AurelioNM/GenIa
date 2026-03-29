from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from models.customer import Customer
from models.product import Product
import ulid


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()), description="Product ulid")
    customer: Customer
    products: List[Product]
    total_value: float
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)


class OrdersPage(BaseModel):
    orders: List[Order]


class MostPurchasedCategory(BaseModel):
    category: str
