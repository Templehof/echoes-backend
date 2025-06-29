from functools import lru_cache
from src.config import Settings
from google import genai

CACHE_MAX_SIZE = 1000


def get_settings():
    return Settings()


settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)


@lru_cache(maxsize=CACHE_MAX_SIZE)
def get_short_story_about_location(lat: float, long: float):
    genai_resul = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=["In no more than 200 words",
                  f"Create a short summary of what you know about this location: latitude: {lat}, longitude: {long}, "
                  f"try to identify the closest notable settlement.",
                  "Aim to adjust the text to the target audience of people who are tourists or history enthusiasts in "
                  "the area and would like to learn more about the history of this location",
                  "if the location is unknown to you say something witty. Do your best to remember what notable "
                  "people were born in the location or what notable events happened there! DO NOT USE markup signs "
                  "such as ** and any others."],
    )
    return genai_resul.text


@lru_cache(maxsize=CACHE_MAX_SIZE)
def get_google_maps_link_with_notable_locations(lat: float, long: float):
    genai_resul = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=[f"Given the coordinates latitude: {lat}, longitude: {long}, Identify the largest settlement (city "
                  f"or town) within a 50-mile radius. Then, select 3–5 notable locations (e.g., landmarks, museums, "
                  f"parks, or historical sites) within or near that settlement. For each location, determine its "
                  f"precise coordinates. Generate a Google Maps link that includes the largest settlement and the "
                  f"selected notable locations in the format: https://www.google.com/maps/dir/[Settlement]/["
                  f"Location1]/[Location2]/[Location3]/... Ensure: Location names are URL-encoded (spaces replaced "
                  f"with + or %20, special characters encoded). The settlement is the starting point, followed by the "
                  f"notable locations in a logical order (e.g., proximity or popularity). The link is valid and "
                  f"functional when opened in a browser. If the coordinates are in a remote area with no significant "
                  f"settlement nearby, identify notable locations within a 100-mile radius and include the nearest "
                  f"settlement, noting its distance. Return ONLY the google maps link!"],
    )
    return genai_resul.text
