from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    region: str = Field(..., min_length=1, max_length=100)
    language: list[str] = Field(default_factory=list)
    currency: str = Field(..., min_length=1, max_length=10)
    best_season: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=1000)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    country: str | None = Field(default=None, min_length=1, max_length=100)
    region: str | None = Field(default=None, min_length=1, max_length=100)
    language: list[str] | None = None
    currency: str | None = Field(default=None, min_length=1, max_length=10)
    best_season: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, min_length=1, max_length=1000)


class CityResponse(CityBase):
    id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
