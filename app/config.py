import json
from functools import lru_cache
from pathlib import Path, PosixPath
from typing import Any, Dict, List, Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    service_api_key: str
    cors_origins: Union[str, List[str]]
    charts_output_dir: Union[PosixPath, str]
    tables_output_dir: Union[PosixPath, str]
    indo_province_geojson: Union[PosixPath, str, Dict[Any, Any]]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    settings = Settings()
    settings.cors_origins = settings.cors_origins.split(";")
    settings.charts_output_dir = Path(settings.charts_output_dir)
    settings.tables_output_dir = Path(settings.tables_output_dir)

    with open(settings.indo_province_geojson, "r") as f:
        settings.indo_province_geojson = json.loads(f.read())

    return settings
