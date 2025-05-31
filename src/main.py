from fastapi import FastAPI
from src.api.v1.endpoints.location import router as location_router
from src.config import Settings


def get_settings():
    return Settings()


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0"
)

app.include_router(
    location_router,
    prefix="/api/v1",
    tags=["location"]
)


@app.get("/")
def read_root():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug
    }
