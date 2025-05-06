from fastapi import FastAPI
from src.api.v1.endpoints.location import router as location_router

app = FastAPI(
    title="Echoes Location API",
    description="API for identifying locations by name or coordinates for use with echoes application",
    version="1.0.0")

app.include_router(
    location_router,
    prefix="/api/v1",
    tags=["location"]
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
