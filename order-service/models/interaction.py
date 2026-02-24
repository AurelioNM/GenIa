from typing import List

from pydantic import BaseModel, Field
from enum import Enum


class IntentationEnum(str, Enum):
    PURCHASE_PRODUCT = "PURCHASE_PRODUCT"
    SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER = "SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER"
    SUGGEST_PRODUCT_BASED_ON_CATEGORY = "SUGGEST_PRODUCT_BASED_ON_CATEGORY"
    SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY = "SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY"
    UNKNOWN = "UNKNOWN"


class InteractionOutput(BaseModel):
    output: str = Field(description="LLM response to the customer input")
    intation: IntentationEnum = Field(description="Intation of interaction")
    products_names: List[str] | None = Field(
        default=None, description="List of products names"
    )


class InteractionRequest(BaseModel):
    customer_email: str = Field(description="Customer email")
    input: str = Field(description="Customer input to chat")
