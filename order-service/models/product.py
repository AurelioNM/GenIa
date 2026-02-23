from typing import List

from pydantic import BaseModel, Field
import ulid


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()), description="Product ulid")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(gt=0, description="The price must be greater than zero")
    quantity: int = Field(description="Product quantity")


class ProductList(BaseModel):
    products: List[Product]
