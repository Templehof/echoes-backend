from fastapi import APIRouter
from src.models.LocationModels import FullLocationResponse, LocationRequestByName, LocationRequestByCoordinates
from src.services.locationServices import identify_full_location_by_name, identify_full_location_by_coordinates

router = APIRouter()


@router.post("/location/by-name", response_model=FullLocationResponse)
async def get_location_by_name(request: LocationRequestByName):
    data = identify_full_location_by_name(request.name)
    result = data[0]
    return FullLocationResponse(
        name=result["formatted_address"][:200],  # Truncate to ensure max_length
        place_id=result.get("place_id"),  # Safe access for optional field
        latitude=result["geometry"]["location"]["lat"],
        longitude=result["geometry"]["location"]["lng"]
    )


@router.post("/location/by-coordinates", response_model=FullLocationResponse)
async def get_location_by_coordinates(request: LocationRequestByCoordinates):
    data = identify_full_location_by_coordinates(request.longitude, request.latitude)
    result = data[0]
    return FullLocationResponse(
        name=result["formatted_address"],
        place_id=result.get("place_id"),  # Use .get() for optional field
        latitude=result["geometry"]["location"]["lat"],
        longitude=result["geometry"]["location"]["lng"]
    )
