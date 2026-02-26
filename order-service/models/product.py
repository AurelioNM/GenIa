from typing import List

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(description="Product ulid")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(description="Product price")
    category: str = Field(description="Product category")
    quantity: int | None = None


class ProductList(BaseModel):
    products: List[Product]


class ProductNames(BaseModel):
    names: List[str] = Field(description="List of product names")


class ProductSummary(BaseModel):
    name: str = Field(description="Product name")
    description: str | None = None
    price: float = Field(description="Product price")
