from pathlib import Path, PosixPath

import pandas as pd


def serialize_data(
    df: pd.DataFrame, filename=str, output_dir: PosixPath = Path(".")
):
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / filename

    df.to_parquet(output_path.with_suffix(".gzip"), compression="gzip")
