from pathlib import Path, PosixPath
from typing import Optional, Union

from pydantic import BaseModel, root_validator, validator

from app.constant import ChartTypes
from app.schema.params import BarChartParams

TYPE_PARAMS_MAP = {ChartTypes.bar: BarChartParams}


def _cast_to_posix_path(str):
    return Path(str)


class ChartBuilderRequest(BaseModel):
    input_path: Union[str, PosixPath]
    output_path: Union[str, PosixPath]
    chart_type: ChartTypes
    graph_params: Union[BarChartParams]
    title: Optional[str] = None

    _cast_input_path = validator("input_path", allow_reuse=True)(
        _cast_to_posix_path
    )
    _cast_output_path = validator("output_path", allow_reuse=True)(
        _cast_to_posix_path
    )

    @root_validator
    def check_type_and_params_pair(cls, values):
        assert (
            type(values["graph_params"])
            == TYPE_PARAMS_MAP[values["chart_type"]]
        )

        return values
