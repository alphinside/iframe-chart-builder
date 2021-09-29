from http import HTTPStatus
from pathlib import Path
from typing import Tuple

import config
import pandas as pd
from fastapi import HTTPException

from app.config import get_settings
from app.constant import (
    STANDARD_CHARTS_CONFIG,
    STANDARD_DATA_FILENAME,
    ResourceType,
)
from app.schema.params import AppliedFilters
from app.schema.requests import BaseChartBuilderRequest
from app.utils import (
    check_validate_chart_config,
    construct_standard_dash_url,
    read_data,
)

config.table_dfs = {}
config.table_snippets = {}
config.charts = {}


def get_data(table_name: str, rewrite: bool = False) -> pd.DataFrame:
    if table_name not in config.table_dfs.keys() or rewrite is True:
        data_path = (
            get_settings().tables_output_dir
            / Path(table_name)
            / STANDARD_DATA_FILENAME
        )

        if not data_path.exists():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"table `{table_name}` not found, "
                "please upload it first",
            )

        config.table_dfs[table_name] = read_data(data_path)
        config.table_dfs[table_name] = config.table_dfs[table_name].loc[
            :, ~config.table_dfs[table_name].columns.str.contains("^Unnamed")
        ]

    return config.table_dfs[table_name].copy()


def apply_filter(
    df: pd.DataFrame, applied_filters: AppliedFilters
) -> pd.DataFrame:
    for column_filter in applied_filters.categorical:
        df = df.query(f"{column_filter.column} == {column_filter.values}")

    for column_filter in applied_filters.numerical:
        if (
            column_filter.values_min is not None
            and column_filter.values_min >= column_filter.column_min
        ):
            df = df.query(
                f"{column_filter.column} >= {column_filter.values_min}"
            )

        if (
            column_filter.values_max is not None
            and column_filter.values_max <= column_filter.column_max
        ):
            df = df.query(
                f"{column_filter.column} <= {column_filter.values_max}"
            )

    return df


def register_table_path(table_name: str, table_snippet_url: str):
    config.table_snippets[table_snippet_url] = table_name


def register_chart_path(chart_name: str, chart_url: str):
    config.charts[chart_url] = chart_name


def create_dir_dependencies():
    get_settings().charts_output_dir.mkdir(exist_ok=True)
    get_settings().tables_output_dir.mkdir(exist_ok=True)


def populate_persisted_data():
    populate_persisted_tables()
    populate_persisted_charts()


def populate_persisted_tables():
    for table_name_path in get_settings().tables_output_dir.iterdir():
        data_path = table_name_path / STANDARD_DATA_FILENAME
        table_name = table_name_path.name

        if data_path.exists():
            table_snippet_url = construct_standard_dash_url(
                name=table_name, resource_type=ResourceType.table
            )
            register_table_path(
                table_name=table_name, table_snippet_url=table_snippet_url
            )


def populate_persisted_charts():
    for chart_name_path in get_settings().charts_output_dir.iterdir():
        data_path = chart_name_path / STANDARD_CHARTS_CONFIG
        chart_name = chart_name_path.name

        if data_path.exists():
            chart_url = construct_standard_dash_url(
                name=chart_name, resource_type=ResourceType.chart
            )
            register_chart_path(chart_name=chart_name, chart_url=chart_url)


def get_charts_meta(
    chart_name: str,
) -> Tuple[pd.DataFrame, BaseChartBuilderRequest]:
    config_model = check_validate_chart_config(chart_name)
    df = get_data(config_model.table_name)

    return (df, config_model)
