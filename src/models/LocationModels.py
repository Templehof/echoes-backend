from pydantic import BaseModel, Field, field_validator


class LocationRequestByName(BaseModel):
    name: str = Field(..., max_length=100, min_length=1, description="Location name (e.g., 'New York, NY')")


class LocationRequestByCoordinates(BaseModel):
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")


class FullLocationResponse(BaseModel):
    name: str = Field(..., max_length=200, description="Location name or formatted address")
    place_id: str | None = Field(None, description="Google Maps Place ID, if available")
    longitude: float = Field(..., description="Longitude in degrees")
    latitude: float = Field(..., description="Latitude in degrees")
