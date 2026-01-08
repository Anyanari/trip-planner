from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    osm_nominatim_url: str = "https://nominatim.openstreetmap.org"
    app_name: str = "Trip Planner API"
    debug: bool = True
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорировать лишние поля

settings = Settings()
