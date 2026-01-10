from typing import Optional

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="sqlite:///./app.db",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )
    osm_nominatim_url: str = Field(
        default="https://nominatim.openstreetmap.org",
        validation_alias=AliasChoices("OSM_NOMINATIM_URL", "osm_nominatim_url"),
    )
    app_name: str = "Trip Planner API"
    debug: bool = True
    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
