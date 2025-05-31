import googlemaps
from src.config import Settings


def get_settings():
    return Settings()


settings = get_settings()
gmaps = googlemaps.Client(key=settings.google_maps_api_key)


def identify_full_location_by_name(name: str) -> dict:
    geocode_result = gmaps.geocode(name)
    return geocode_result


def identify_full_location_by_coordinates(long: float, lat: float):
    reverse_geocode_result = gmaps.reverse_geocode((lat, long))
    return reverse_geocode_result
