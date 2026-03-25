from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AttractionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    category: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=200)
    rating: float = Field(..., ge=0, le=5)
    ticket_price_eur: float = Field(..., ge=0)
    is_free: bool
    recommended_visit_hours: float = Field(..., gt=0, le=24)
    tags: list[str] = Field(default_factory=list)
    description: str = Field(..., min_length=1, max_length=1000)


class AttractionCreate(AttractionBase):
    city_id: str | None = Field(default=None, min_length=1)
    city_name: str | None = Field(default=None, min_length=1, max_length=100)

    @model_validator(mode="after")
    def validate_city_reference(self) -> "AttractionCreate":
        if not self.city_id and not self.city_name:
            raise ValueError("Either city_id or city_name must be provided.")
        return self


class AttractionUpdate(BaseModel):
    city_id: str | None = Field(default=None, min_length=1)
    city_name: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=150)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    address: str | None = Field(default=None, min_length=1, max_length=200)
    rating: float | None = Field(default=None, ge=0, le=5)
    ticket_price_eur: float | None = Field(default=None, ge=0)
    is_free: bool | None = None
    recommended_visit_hours: float | None = Field(default=None, gt=0, le=24)
    tags: list[str] | None = None
    description: str | None = Field(default=None, min_length=1, max_length=1000)


class AttractionResponse(AttractionBase):
    id: str
    city_id: str
    city_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
