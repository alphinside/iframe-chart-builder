import urllib
from pathlib import Path, PosixPath
from typing import Type, Union

import pandas as pd
from pydantic import BaseModel

from app.constant import DASH_MOUNT_ROUTE
from app.schema.requests import ChartBuilderRequest


def serialize_data(
    df: pd.DataFrame, filename=str, output_dir: PosixPath = Path(".")
):
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename

    df.to_parquet(output_path.with_suffix(".gzip"), compression="gzip")


def read_data(path: Union[str, PosixPath]):
    return pd.read_parquet(path)


def serialize_config(
    config: Type[BaseModel],
    output_dir: PosixPath,
    filename: Union[str, PosixPath],
):
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename

    with open(output_path, "w") as f:
        f.write(config.json())


def read_config(path: Union[str, PosixPath]) -> Type[ChartBuilderRequest]:
    return ChartBuilderRequest.parse_file(path)


def construct_standard_dash_url(name: str, route: str) -> str:
    url = Path(DASH_MOUNT_ROUTE + route) / name
    url = urllib.parse.quote(str(url))

    return url
