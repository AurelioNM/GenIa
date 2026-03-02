from typing import List

from pydantic import BaseModel, Field
from models.order_request import ProductRequest


class PurchaseProductToolInput(BaseModel):
    email: str = Field(description="Customer email")
    products: List[ProductRequest] = Field(description="List of products")
