from collections import Counter
from typing import Any, List, Optional, Union

from pydantic import BaseModel, validator

from app.constant import MAX_NUMBER_FILTERS, DataTypes


class ColumnFilter(BaseModel):
    column: str
    type: DataTypes


class MinMaxNumericalFilterState(BaseModel):
    column: str
    min: Union[int, float, None] = None
    max: Union[int, float, None] = None


class CategoricalFilterState(BaseModel):
    column: str
    values: List[Any] = []


class AppliedFilters(BaseModel):
    categorical: List[CategoricalFilterState] = []
    numerical: List[MinMaxNumericalFilterState] = []


class BaseChartParams(BaseModel):
    title: Optional[str] = None
    filters: List[ColumnFilter] = []

    @validator("filters")
    def validate_and_limit_filters(cls, v):
        if len(v) > MAX_NUMBER_FILTERS:
            v = v[:MAX_NUMBER_FILTERS]

        declared_cols = Counter([col_filter.column for col_filter in v])
        duplicate_cols = [
            column for column, count in declared_cols.items() if count > 1
        ]

        if len(duplicate_cols) != 0:
            raise ValueError(
                f"filter contain duplicate columns {duplicate_cols}"
            )

        return v


class BarChartParams(BaseChartParams):
    column_for_x: str
    column_for_y: Union[List[str], str]
    column_for_color: Optional[str] = None

    @validator("column_for_y")
    def check_and_cast_column_for_y(cls, v):
        if len(v) == 0:
            raise ValueError("`column_for_y` cannot be empty")

        if len(v) == 1:
            v = v[0]

        return v


class ChoroplethMapParams(BaseChartParams):
    column_for_province: str
    column_for_color: str
    zoom_level: int = 4
