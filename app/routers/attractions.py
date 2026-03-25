from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.core.database import attractions_collection, cities_collection
from app.schemas.attraction import (
    AttractionCreate,
    AttractionResponse,
    AttractionUpdate,
)
from app.utils.bson import parse_object_id, serialize_mongo_document

router = APIRouter(prefix="/api/v1/attractions", tags=["Attractions"])


def ensure_city_exists(city_id: str) -> None:
    city = cities_collection.find_one({"_id": parse_object_id(city_id)})
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")


def resolve_city_reference(city_id: str | None = None, city_name: str | None = None) -> str:
    if city_id:
        ensure_city_exists(city_id)
        return city_id

    city_document = cities_collection.find_one({"name": city_name})
    if city_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return str(city_document["_id"])


def build_city_filter(city: str) -> str:
    if not city:
        return city

    if len(city) == 24:
        try:
            parse_object_id(city)
            return city
        except HTTPException:
            pass

    city_document = cities_collection.find_one({"name": city})
    if city_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return str(city_document["_id"])


def enrich_attraction(document: dict | None) -> dict | None:
    serialized = serialize_mongo_document(document)
    if serialized is None:
        return None

    city_document = cities_collection.find_one({"_id": parse_object_id(serialized["city_id"])})
    serialized["city_name"] = city_document["name"] if city_document else None
    return serialized


@router.get("", response_model=list[AttractionResponse])
def list_attractions(
    city: str | None = Query(default=None, description="Filter by city id or city name."),
    category: str | None = Query(default=None, description="Filter by category."),
    is_free: bool | None = Query(default=None, description="Filter by free admission."),
) -> list[dict]:
    filters: dict = {}
    if city:
        filters["city_id"] = build_city_filter(city)
    if category:
        filters["category"] = category
    if is_free is not None:
        filters["is_free"] = is_free

    attractions = attractions_collection.find(filters).sort("name", 1)
    return [enrich_attraction(attraction) for attraction in attractions]


@router.get("/{attraction_id}", response_model=AttractionResponse)
def get_attraction(attraction_id: str) -> dict:
    attraction = attractions_collection.find_one({"_id": parse_object_id(attraction_id)})
    if attraction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attraction not found.",
        )
    return enrich_attraction(attraction)


@router.post("", response_model=AttractionResponse, status_code=status.HTTP_201_CREATED)
def create_attraction(payload: AttractionCreate) -> dict:
    now = datetime.now(timezone.utc)
    document = payload.model_dump()
    document["city_id"] = resolve_city_reference(
        city_id=document.pop("city_id", None),
        city_name=document.pop("city_name", None),
    )
    document["created_at"] = now
    document["updated_at"] = now

    result = attractions_collection.insert_one(document)
    created_attraction = attractions_collection.find_one({"_id": result.inserted_id})
    return enrich_attraction(created_attraction)


@router.patch("/{attraction_id}", response_model=AttractionResponse)
def update_attraction(attraction_id: str, payload: AttractionUpdate) -> dict:
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update.",
        )

    if "city_id" in update_data or "city_name" in update_data:
        update_data["city_id"] = resolve_city_reference(
            city_id=update_data.pop("city_id", None),
            city_name=update_data.pop("city_name", None),
        )

    update_data["updated_at"] = datetime.now(timezone.utc)
    attraction_object_id = parse_object_id(attraction_id)
    result = attractions_collection.update_one(
        {"_id": attraction_object_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attraction not found.",
        )

    updated_attraction = attractions_collection.find_one({"_id": attraction_object_id})
    return enrich_attraction(updated_attraction)


@router.delete("/{attraction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attraction(attraction_id: str) -> Response:
    result = attractions_collection.delete_one({"_id": parse_object_id(attraction_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attraction not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
