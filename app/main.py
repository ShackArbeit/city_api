from fastapi import FastAPI

from app.core.config import get_settings
from app.routers.attractions import router as attractions_router
from app.routers.cities import router as cities_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {"message": "Europe Travel API is running."}


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(cities_router)
app.include_router(attractions_router)
