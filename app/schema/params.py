from collections import Counter
from typing import Any, List, Optional, Union

import plotly.express as px
from pydantic import BaseModel, validator
from pydantic.class_validators import root_validator

from app.constant import (
    MAX_NUMBER_FILTERS,
    BarMode,
    BarOrientation,
    BarPercentageColumnBase,
    DataTypes,
    FillEnum,
    PlotlyColorGroup,
)


class StyleQueryParam(BaseModel):
    width: Optional[str] = None
    height: Optional[str] = None

    @root_validator(pre=True)
    def cast_list_to_str(cls, values):
        if "width" in values.keys():
            if isinstance(values["width"], list):
                values["width"] = values["width"][0]

        if "height" in values.keys():
            if isinstance(values["height"], list):
                values["height"] = values["height"][0]

        return values


class ColumnFilter(BaseModel):
    column: str
    type: DataTypes


class MinMaxNumericalFilterState(BaseModel):
    column: str
    column_min: Union[int, float]
    column_max: Union[int, float]
    values_min: Union[int, float, None] = None
    values_max: Union[int, float, None] = None


class CategoricalFilterState(BaseModel):
    column: str
    values: List[Any] = []


class AppliedFilters(BaseModel):
    categorical: List[CategoricalFilterState] = []
    numerical: List[MinMaxNumericalFilterState] = []


class BuiltInColors(BaseModel):
    group: PlotlyColorGroup
    color_name: str

    @root_validator
    def check_if_color_exist_in_group(cls, values):
        group = values["group"]
        color_name = values["color_name"]

        if not hasattr(getattr(px.colors, group), color_name):
            raise ValueError(
                f"built in color `{color_name}` not found "
                f"in color group `{group}`"
            )

        return values


class ColorOptions(BaseModel):
    discrete: Optional[Union[BuiltInColors, List[str]]] = None
    continuous: Optional[Union[BuiltInColors, List[str]]] = None

    @validator("discrete")
    def validate_discrete_color_category(cls, v):
        if isinstance(v, BuiltInColors):
            group = v.group
            color_name = v.color_name

            v = getattr(getattr(px.colors, group), color_name)

        return v

    @validator("continuous")
    def validate_continuous_color_category(cls, v):
        if isinstance(v, BuiltInColors):
            if v.group == PlotlyColorGroup.qualitative:
                raise ValueError(
                    "qualitative color group cannot be used "
                    "for continuous color type"
                )

            group = v.group
            color_name = v.color_name

            v = getattr(getattr(px.colors, group), color_name)

        return v


class BaseChartParams(BaseModel):
    title: Optional[str] = None
    filters: List[ColumnFilter] = []
    color_opt: ColorOptions = ColorOptions()

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
    column_for_x: Union[List[str], str]
    column_for_y: Union[List[str], str]
    column_for_color: Optional[str] = None
    barmode: BarMode = BarMode.stack
    orientation: BarOrientation = BarOrientation.v
    percentage_column_base: BarPercentageColumnBase = (
        BarPercentageColumnBase.column_for_xy
    )

    @validator("column_for_x")
    def check_and_cast_column_for_x(cls, v):
        if isinstance(v, list) and len(v) == 0:
            raise ValueError("`column_for_x` cannot be empty")

        if isinstance(v, list) and len(v) == 1:
            v = v[0]

        return v

    @validator("column_for_y")
    def check_and_cast_column_for_y(cls, v):
        if isinstance(v, list) and len(v) == 0:
            raise ValueError("`column_for_y` cannot be empty")

        if isinstance(v, list) and len(v) == 1:
            v = v[0]

        return v

    @root_validator(pre=True)
    def check_color_column_in_wide_format(cls, values):
        column_for_x = values["column_for_x"]
        column_for_y = values["column_for_y"]
        column_for_color = values["column_for_color"]

        if (
            isinstance(column_for_x, list) or isinstance(column_for_y, list)
        ) and (column_for_color is not None):
            raise ValueError(
                "`column_for_color` cannot be used in wide bar format, please "
                "delete it from config"
            )

        return values


class ChoroplethMapParams(BaseChartParams):
    column_for_location: str
    column_for_color: str
    zoom_level: int = 4


class BubbleMapParams(BaseChartParams):
    column_for_latitude: str
    column_for_longitude: str
    column_for_color: Optional[str] = None
    column_for_size: Optional[str] = None
    zoom_level: int = 4

    @root_validator
    def color_or_size_must_exist(cls, values):
        if (
            values["column_for_color"] is None
            and values["column_for_size"] is None
        ):
            raise ValueError("column for size or color cannot both empty")

        return values


class BubbleChartParams(BaseChartParams):
    column_for_x: str
    column_for_y: str
    column_for_size: Optional[str] = None
    column_for_color: Optional[str] = None
    column_for_hover_name: Optional[str] = None
    apply_log_x: bool = False
    bubble_size_max: int = 60


class LineChartParams(BaseChartParams):
    column_for_x: str
    column_for_y: str
    column_for_color: Optional[str] = None


class PieChartParams(BaseChartParams):
    column_for_values: str
    column_for_names: str
    center_hole_ratio: float = 0.0

    @validator("center_hole_ratio")
    def check_and_cast_column_for_y(cls, v):
        if v < 0 or v > 1:
            raise ValueError("center_hole_ratio must be between 0 and 1")

        return v


class WindroseChartParams(BaseChartParams):
    column_for_radius: str
    column_for_theta: str
    column_for_color: Optional[str] = None


class SunburstChartParams(BaseChartParams):
    column_for_path: List[str]
    column_for_values: str
    column_for_color: Optional[str] = None


class RadarChartParams(BaseChartParams):
    column_for_radius: str
    column_for_theta: List[str]
    fill: Optional[FillEnum] = None
