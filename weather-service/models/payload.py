from pydantic import BaseModel, Field


class ProcessCityPayload(BaseModel):
    name: str = Field(description="City name")
