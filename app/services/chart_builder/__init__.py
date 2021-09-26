from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import List

import pandas as pd
from fastapi import HTTPException
from pandas.api.types import is_numeric_dtype

from app.constant import DataTypes
from app.errors import COLUMN_INVALID_TYPE_ERROR, COLUMN_NOT_FOUND_ERROR
from app.schema.params import ColumnFilter


class ChartBuilderInterface(ABC):
    @abstractmethod
    def validate_columns(self):
        pass

    @abstractmethod
    def build_chart(self):
        pass

    def validate_filters(self, df: pd.DataFrame, filters: List[ColumnFilter]):
        if len(filters) == 0:
            return

        columns_not_found = []
        columns_invalid_type = []

        for filter in filters:
            if filter.column not in df.columns:
                columns_not_found.append(filter.column)

            if filter.type == DataTypes.numerical:
                if not is_numeric_dtype(df[filter.column]):
                    columns_invalid_type.append(
                        (filter.column, filter.type.name)
                    )

        if len(columns_not_found) != 0 or len(columns_invalid_type) != 0:
            err_messages = []
            if len(columns_not_found) != 0:
                err_messages.append(
                    COLUMN_NOT_FOUND_ERROR.format_map(
                        {"column_names": columns_not_found}
                    )
                )

            if len(columns_invalid_type) != 0:
                err_messages.append(
                    COLUMN_INVALID_TYPE_ERROR.format_map(
                        {"column_types": columns_invalid_type}
                    )
                )

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=", ".join(err_messages),
            )
