from pydantic import BaseModel, Field


class Customer(BaseModel):
    id: str = Field(description="Customer ulid")
    name: str = Field(description="Customer name")
    email: str = Field(description="Customer email")
