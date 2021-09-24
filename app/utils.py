from pathlib import Path, PosixPath
from typing import Union

import pandas as pd
from omegaconf import DictConfig, OmegaConf


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
