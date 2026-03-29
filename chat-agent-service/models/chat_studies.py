from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class ChatStudiesInput(BaseModel):
    input: str = Field(description="Input for chat studiesmn,k")


class ChatStudiesOutput(BaseModel):
    output: str = Field(description="Output for chat_interaction generation")


class ProductReviewOutput(BaseModel):
    gift: bool = Field(description="True if purchased as a gift, False otherwise")
    delivery_days: int = Field(description="Number of days to arrive, -1 if not found")
    price_value: List[str] = Field(description="Sentences mentioning value or price")
