import urllib
from pathlib import Path, PosixPath
from typing import Union

import pandas as pd
from omegaconf import DictConfig, OmegaConf

from app.constant import DASH_MOUNT_ROUTE, TABLES_ROUTE


def serialize_data(
    df: pd.DataFrame, filename=str, output_dir: PosixPath = Path(".")
):
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename

    df.to_parquet(output_path.with_suffix(".gzip"), compression="gzip")


def serialize_config(
    config: DictConfig, output_dir: PosixPath, filename: Union[str, PosixPath]
):
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename

    OmegaConf.save(config=config, f=output_path)


def construct_standard_table_url(table_name: str) -> str:
    table_snippet_url = Path(DASH_MOUNT_ROUTE + TABLES_ROUTE) / table_name
    table_snippet_url = urllib.parse.quote(str(table_snippet_url))

    return table_snippet_url
