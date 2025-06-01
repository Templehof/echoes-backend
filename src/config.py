from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os


def get_secret_or_env(key: str, default=None):
    """Try to read from Docker secret, fallback to env var"""
    # Try Docker secret first (lowercase)
    secret_file = Path(f"/run/secrets/{key.lower()}")
    if secret_file.exists():
        return secret_file.read_text().strip()

    # Fallback to environment variable (uppercase)
    return os.getenv(key.upper(), default)


class Settings(BaseSettings):
    google_maps_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    app_name: Optional[str] = None
    environment: Optional[str] = None
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Override with Docker secrets if available
        self.google_maps_api_key = get_secret_or_env("GOOGLE_MAPS_API_KEY", self.google_maps_api_key)
        self.gemini_api_key = get_secret_or_env("GEMINI_API_KEY", self.gemini_api_key)
        self.app_name = get_secret_or_env("APP_NAME", self.app_name)
        self.environment = get_secret_or_env("ENVIRONMENT", self.environment)
        debug_value = get_secret_or_env("DEBUG", str(self.debug))
        self.debug = debug_value.lower() in ('true', '1', 'yes') if debug_value else self.debug
