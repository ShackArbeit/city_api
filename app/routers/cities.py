from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status

from app.core.database import cities_collection
from app.schemas.city import CityCreate, CityResponse, CityUpdate
from app.utils.bson import parse_object_id, serialize_mongo_document

router = APIRouter(prefix="/api/v1/cities", tags=["Cities"])


@router.get("", response_model=list[CityResponse])
def list_cities() -> list[dict]:
    cities = cities_collection.find().sort("name", 1)
    return [serialize_mongo_document(city) for city in cities]


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: str) -> dict:
    city = cities_collection.find_one({"_id": parse_object_id(city_id)})
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return serialize_mongo_document(city)


@router.post("", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(payload: CityCreate) -> dict:
    now = datetime.now(timezone.utc)
    document = payload.model_dump()
    document["created_at"] = now
    document["updated_at"] = now

    result = cities_collection.insert_one(document)
    created_city = cities_collection.find_one({"_id": result.inserted_id})
    return serialize_mongo_document(created_city)


@router.patch("/{city_id}", response_model=CityResponse)
def update_city(city_id: str, payload: CityUpdate) -> dict:
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update.",
        )

    update_data["updated_at"] = datetime.now(timezone.utc)
    result = cities_collection.update_one(
        {"_id": parse_object_id(city_id)},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    updated_city = cities_collection.find_one({"_id": parse_object_id(city_id)})
    return serialize_mongo_document(updated_city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: str) -> Response:
    result = cities_collection.delete_one({"_id": parse_object_id(city_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
