from datetime import datetime
from pydantic import BaseModel, Field
import ulid


class Customer(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ulid.new()), description="Id on ulid pattern"
    )
    name: str = Field(..., description="Name")
    email: str = Field(..., description="Email adress")
    active: bool = Field(default=True, description="Active status")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation date."
    )
    updated_at: datetime | None = Field(default=None, description="Update date.")
