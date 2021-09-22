from typing import List, Optional, Union

from pydantic import BaseModel, root_validator


class BarChartParams(BaseModel):
    column_for_x: str
    column_for_y: Union[str, List[str]]
    column_for_color: Optional[str] = None

    @root_validator
    def check_color_and_y_pair(cls, values):
        if not isinstance(values["column_for_y"], list):
            assert values["column_for_y"] is not None

        return values
