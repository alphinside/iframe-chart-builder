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
    def limit_number_of_filters(cls, v):
        if len(v) > MAX_NUMBER_FILTERS:
            v = v[:MAX_NUMBER_FILTERS]

        return v


class BarChartParams(BaseChartParams):
    column_for_x: str
    column_for_y: Union[str, List[str]]
    column_for_color: Optional[str] = None


class ChoroplethMapParams(BaseChartParams):
    column_for_province: str
    column_for_color: str
    zoom_level: int = 4
