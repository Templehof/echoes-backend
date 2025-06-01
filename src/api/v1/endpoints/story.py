from fastapi import APIRouter
from src.models.LocationModels import LocationRequestByCoordinates
from src.services.aiServices import get_short_story_about_location

router = APIRouter()


@router.post("/story/by-coordinates")
def get_location_by_coordinates(request: LocationRequestByCoordinates):
    data = get_short_story_about_location(request.latitude, request.longitude)
    return data
