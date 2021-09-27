import urllib
from pathlib import Path, PosixPath
from typing import Type, Union

import pandas as pd
from pydantic import BaseModel

from app.config import get_settings
from app.constant import (
    CHARTS_ROUTE,
    DASH_MOUNT_ROUTE,
    STANDARD_CHARTS_CONFIG,
    STANDARD_STYLE_CONFIG,
    TABLES_ROUTE,
)
from app.schema.requests import (
    TYPE_PARAMS_MAP,
    BaseChartBuilderRequest,
    ChartStyle,
)


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


def construct_standard_dash_url(name: str, route: str) -> str:
    url = Path(DASH_MOUNT_ROUTE + route) / name
    url = urllib.parse.quote(str(url))

    return url


def check_validate_chart_config(chart_name: str):
    chart_config_file_path = (
        get_settings().charts_output_dir / chart_name / STANDARD_CHARTS_CONFIG
    )

    if not chart_config_file_path.exists():
        raise FileNotFoundError(
            f"config chart `{chart_name}` not found "
            f"in {chart_config_file_path}"
        )

    base_config = BaseChartBuilderRequest.parse_file(chart_config_file_path)
    base_config.chart_params = TYPE_PARAMS_MAP[
        base_config.chart_type
    ].parse_obj(base_config.chart_params)

    return base_config


def check_validate_style_config(name: str, route: PosixPath):
    if route == CHARTS_ROUTE:
        style_config = (
            get_settings().charts_output_dir / name / STANDARD_STYLE_CONFIG
        )
    elif route == TABLES_ROUTE:
        style_config = (
            get_settings().tables_output_dir / name / STANDARD_STYLE_CONFIG
        )
    else:
        raise Exception(f"style config of {route}{name} not found")

    return ChartStyle.parse_file(style_config)
