from typing import Any

from fastapi import HTTPException, status
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConfigurationError, PyMongoError

from app.core.config import get_settings

settings = get_settings()


def _database_unavailable_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Database is unavailable. Check the MongoDB configuration.",
    )


def get_client() -> MongoClient:
    try:
        return MongoClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    except (ConfigurationError, PyMongoError) as exc:
        raise _database_unavailable_exception() from exc


def get_database() -> Database:
    try:
        return get_client()[settings.db_name]
    except (ConfigurationError, PyMongoError) as exc:
        raise _database_unavailable_exception() from exc


def get_collection(name: str) -> Collection:
    try:
        return get_database()[name]
    except (ConfigurationError, PyMongoError) as exc:
        raise _database_unavailable_exception() from exc


class LazyCollection:
    def __init__(self, name: str) -> None:
        self.name = name

    def _collection(self) -> Collection:
        return get_collection(self.name)

    def __getattr__(self, attribute: str) -> Any:
        return getattr(self._collection(), attribute)


cities_collection = LazyCollection("cities")
attractions_collection = LazyCollection("attractions")
