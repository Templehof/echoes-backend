from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_maps_api_key: Optional[str] = None
    app_name: Optional[str] = None
    environment: Optional[str] = None
    debug: bool = True
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )
