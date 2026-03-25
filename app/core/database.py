from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.config import get_settings

settings = get_settings()
client = MongoClient(settings.mongodb_url)
database: Database = client[settings.db_name]


def get_collection(name: str) -> Collection:
    return database[name]


cities_collection = get_collection("cities")
attractions_collection = get_collection("attractions")
