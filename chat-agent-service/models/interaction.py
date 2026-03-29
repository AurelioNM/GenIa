from pydantic import BaseModel, Field
from enum import Enum


class IntationEnum(str, Enum):
    PURCHASE_PRODUCT = "PURCHASE_PRODUCT"
    SUGGEST_PRODUCT_BASED_ON_CATEGORY = "SUGGEST_PRODUCT_BASED_ON_CATEGORY"
    SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY = "SUGGEST_PRODUCT_BASED_ON_ORDER_HISTORY"
    SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER = "SUGGEST_DAY_TO_GO_OUT_BASED_ON_WEATHER"
    TARANTINO_QUESTION = "TARANTINO_QUESTION"
    UNKNOWN = "UNKNOWN"


class InteractionRequest(BaseModel):
    customer_email: str = Field(description="Customer email")
    input: str = Field(description="Customer input to chat")


class InteractionOutputV2(BaseModel):
    output: str = Field(description="LLM response to the customer input")
