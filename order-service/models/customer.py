from pydantic import BaseModel, Field
import ulid


class Customer(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ulid.new()), description="Customer ulid"
    )
    name: str = Field(description="Customer name")
    email: str = Field(description="Customer email")
