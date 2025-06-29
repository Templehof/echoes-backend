from fastapi import APIRouter
from src.models.LocationModels import LocationRequestByCoordinates
from src.services.aiServices import get_short_story_about_location, get_google_maps_link_with_notable_locations

router = APIRouter()


@router.post("/story/by-coordinates")
def get_story_by_coordinates(request: LocationRequestByCoordinates):
    data = get_short_story_about_location(request.latitude, request.longitude)
    return data


@router.post("/story/link-by-coordinates")
def get_story_by_coordinates(request: LocationRequestByCoordinates):
    data = get_google_maps_link_with_notable_locations(request.latitude, request.longitude)
    return data
