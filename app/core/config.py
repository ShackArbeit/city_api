from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Europe Travel API"
    app_version: str = "1.0.0"
    app_description: str = "A demo RESTful API for European travel cities and attractions."
    mongodb_url: str = Field(..., alias="MONGODB_URL")
    db_name: str = Field(default="europe_travel_api", alias="DB_NAME")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
