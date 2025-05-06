from fastapi import APIRouter
from src.models.LocationModels import FullLocationResponse, LocationRequestByName, LocationRequestByCoordinates
from src.services.locationServices import identify_full_location_by_name, identify_full_location_by_coordinates

router = APIRouter()


@router.post("/location/by-name", response_model=FullLocationResponse)
async def get_location_by_name(request: LocationRequestByName):
    data = identify_full_location_by_name(request.name)
    return FullLocationResponse(**data)


@router.post("/location/by-coordinates", response_model=FullLocationResponse)
async def get_location_by_coordinates(request: LocationRequestByCoordinates):
    data = identify_full_location_by_coordinates(request.longitude, request.latitude)
    return FullLocationResponse(**data)
