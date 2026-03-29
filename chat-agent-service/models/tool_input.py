from typing import List

from pydantic import BaseModel, Field
from models.order_request import ProductRequest
from enum import Enum


class PurchaseProductToolInput(BaseModel):
    email: str = Field(description="Customer email")
    products: List[ProductRequest] = Field(description="List of products")


class SuggestProductOnCategoryToolInput(BaseModel):
    category: str = Field(
        description="Product category to suggest products from. Must be on uppercase"
    )


class SuggestProductOnHistoryToolInput(BaseModel):
    email: str = Field(description="Customer email")


class QuestionSubjectEnum(str, Enum):
    TARANTINO = "TARANTINO"


class QuestionAndAnswerToolInput(BaseModel):
    question: str = Field(description="The question asked by the customer")
    subject: QuestionSubjectEnum = Field(
        description="The subject of the question asked by the customer"
    )
