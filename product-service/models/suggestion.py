from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class SuggestionInput(BaseModel):
    input: str = Field(description="Input for suggestion generation")


class SuggestionOutput(BaseModel):
    output: str = Field(description="Output for suggestion generation")


class ProductReviewOutput(BaseModel):
    gift: bool = Field(description="True if purchased as a gift, False otherwise")
    delivery_days: int = Field(description="Number of days to arrive, -1 if not found")
    price_value: List[str] = Field(description="Sentences mentioning value or price")
