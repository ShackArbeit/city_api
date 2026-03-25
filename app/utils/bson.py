from bson import ObjectId
from fastapi import HTTPException, status


def parse_object_id(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MongoDB ObjectId.",
        )
    return ObjectId(value)


def serialize_mongo_document(document: dict | None) -> dict | None:
    if document is None:
        return None

    serialized = dict(document)
    serialized["id"] = str(serialized.pop("_id"))
    return serialized
