from functools import lru_cache
from typing import List, Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    service_api_key: str
    cors_origins: Union[str, List[str]]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    settings = Settings()
    settings.cors_origins = settings.cors_origins.split(";")
    return settings
