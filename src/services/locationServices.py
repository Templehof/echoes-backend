from src.models.LocationModels import FullLocationResponse


def identify_full_location_by_name(name: str):
    resp = {
        "name": "London",
        "latitude": 51.5072,
        "longitude": 0.1276,
        "place_id": None
    }
    return resp


def identify_full_location_by_coordinates(long: float, lat: float):
    resp = {
        "name": "London",
        "latitude": lat,
        "longitude": long,
        "place_id": None
    }
    return resp
