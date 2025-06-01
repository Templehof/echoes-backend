import asyncio
import datetime

from src.services.locationServices import cached_location_by_name, cached_location_by_coordinates

CACHE_TTL_SECONDS = 604800  # 7 days


async def periodic_cache_clear():
    """Clear cache every 7 days"""
    while True:
        await asyncio.sleep(CACHE_TTL_SECONDS)
        cached_location_by_name.cache_clear()
        cached_location_by_coordinates.cache_clear()
        print(f"Cache cleared at {datetime.now()}")
