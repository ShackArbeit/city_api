from bson import ObjectId
from fastapi import HTTPException

from app.utils.bson import parse_object_id, serialize_mongo_document


def test_parse_object_id_accepts_valid_object_id() -> None:
    value = str(ObjectId())

    parsed = parse_object_id(value)

    assert str(parsed) == value


def test_parse_object_id_rejects_invalid_object_id() -> None:
    try:
        parse_object_id("invalid-object-id")
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Invalid MongoDB ObjectId."
    else:
        raise AssertionError("Expected HTTPException for invalid ObjectId.")


def test_serialize_mongo_document_maps_internal_id_to_public_id() -> None:
    document_id = ObjectId()
    serialized = serialize_mongo_document({"_id": document_id, "name": "Paris"})

    assert serialized == {"id": str(document_id), "name": "Paris"}


def test_serialize_mongo_document_returns_none_for_missing_document() -> None:
    assert serialize_mongo_document(None) is None
