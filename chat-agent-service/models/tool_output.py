from typing import List

from pydantic import BaseModel, Field
from models.product import ProductSummary
from models.weather import Weather


class SuggestProductToolOutput(BaseModel):
    products: List[ProductSummary] = Field(
        description="List of products in the category with their names, prices and description"
    )


class SuggestDayAndProductOnWeatherToolOutput(BaseModel):
    forecast: List[Weather] = Field(description="Weather forecast for the next days")
    products: List[ProductSummary] = Field(
        description="List of products in the weather category with their names, prices and description"
    )
