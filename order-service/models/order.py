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
    created_at: datetime = Field(
        default_factory=datetime.now, description="Create product timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="Update product timestamp"
    )


class OrdersPage(BaseModel):
    orders: List[Order]
