from functools import lru_cache
import googlemaps
from src.config import Settings

CACHE_MAX_SIZE = 1000


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


@lru_cache(maxsize=CACHE_MAX_SIZE)
def cached_location_by_name(name: str) -> dict:
    """Cached version of location lookup by name"""
    normalized_name = name.lower().strip()
    data = identify_full_location_by_name(normalized_name)
    return data[0]


@lru_cache(maxsize=CACHE_MAX_SIZE)
def cached_location_by_coordinates(lat: float, lng: float) -> dict:
    """Cached version of location lookup by coordinates"""
    # Round to 6 decimal places for cache key consistency
    rounded_lat = round(lat, 6)
    rounded_lng = round(lng, 6)
    data = identify_full_location_by_coordinates(rounded_lng, rounded_lat)
    return data[0]
