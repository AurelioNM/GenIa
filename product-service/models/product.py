from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
import ulid


class Product(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ulid.new()), description="Id on ulid pattern"
    )
    name: str = Field(description="Name")
    description: str = Field(description="Description")
    price: float = Field(gt=0, description="Price (must be greater than zero)")
    category: str = Field(description="Category")
    active: bool = Field(default=True, description="Active status")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp of creation"
    )
    updated_at: datetime | None = Field(default=None, description="Timestamp of update")


class ProductNames(BaseModel):
    names: List[str] = Field(description="List of product names")


class ProductList(BaseModel):
    products: List[Product]
