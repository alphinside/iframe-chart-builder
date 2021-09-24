from typing import List, Optional, Union

from pydantic import BaseModel, root_validator


class BaseChartParams(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    title: Optional[str] = None


class BarChartParams(BaseChartParams):
    column_for_x: str
    column_for_y: Union[str, List[str]]
    column_for_color: Optional[str] = None

    @root_validator
    def check_color_and_y_pair(cls, values):
        if not isinstance(values["column_for_y"], list):
            assert values["column_for_color"] is not None

        return values


class ChoroplethMapParams(BaseChartParams):
    column_for_province: str
    column_for_color: str
    zoom_level: int = 4
