from src.models.LocationModels import FullLocationResponse


async def identify_full_location_by_name(name: str):
    resp = dict()
    resp.name = name
    resp.latitude = 90.01
    resp.longitude = 90.01
    return resp


async def identify_full_location_by_coordinates(long: float, lat: float):
    resp = dict()
    resp.name = "some location name"
    resp.latitude = lat
    resp.longitude = long
    return resp
