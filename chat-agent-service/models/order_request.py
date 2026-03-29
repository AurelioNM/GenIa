from typing import List

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    name: str = Field(description="Product name")
    quantity: int = Field(description="Product quantity")


class OrderRequest(BaseModel):
    customer_email: str
    products: List[ProductRequest]


class OrderResponse(BaseModel):
    id: str
    total_value: float
