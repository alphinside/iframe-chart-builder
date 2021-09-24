from pathlib import Path

import pandas as pd

from app.config import get_settings
from app.constant import STANDARD_DATA_FILENAME

dfs = {}


def get_data(table_name: str, rewrite: bool = False) -> pd.DataFrame:
    if table_name not in dfs.keys() or rewrite is True:
        data_path = (
            get_settings().tables_output_dir
            / Path(table_name)
            / STANDARD_DATA_FILENAME
        )

        dfs[table_name] = pd.read_parquet(data_path)
        dfs[table_name] = dfs[table_name].loc[
            :, ~dfs[table_name].columns.str.contains("^Unnamed")
        ]

    return dfs[table_name].copy()
