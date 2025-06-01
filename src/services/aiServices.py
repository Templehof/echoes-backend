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
        contents=["In no more than 100 words",
                  f"Create a short summary of what you know about this location: latitude: {lat}, longitude: {long}",
                  "Aim to adjust the text to the target audience of people who are tourists or history enthusiasts in the area and would like to learn more about the history of this location",
                  "if the location is unknown to you say something witty"],
    )
    return genai_resul.text
