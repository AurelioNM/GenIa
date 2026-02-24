from typing import List

from pydantic import BaseModel


class ProductRequest(BaseModel):
    name: str
    quantity: int


class OrderRequest(BaseModel):
    customer_email: str
    products: List[ProductRequest]


class OrderResponse(BaseModel):
    id: str
    total_value: float
