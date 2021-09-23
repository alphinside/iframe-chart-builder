from pathlib import Path, PosixPath
from typing import Any, Dict, Union

from pydantic import BaseModel, root_validator, validator

from app.constant import ChartTypes
from app.schema.params import BarChartParams, ChoroplethMapParams

TYPE_PARAMS_MAP = {
    ChartTypes.bar: BarChartParams,
    ChartTypes.choropleth_map: ChoroplethMapParams,
}


def _cast_to_posix_path(str):
    return Path(str)


class ChartBuilderRequest(BaseModel):
    input_path: Union[str, PosixPath]
    output_path: Union[str, PosixPath]
    chart_type: ChartTypes
    graph_params: Dict[str, Any]

    _cast_input_path = validator("input_path", allow_reuse=True)(
        _cast_to_posix_path
    )
    _cast_output_path = validator("output_path", allow_reuse=True)(
        _cast_to_posix_path
    )

    @root_validator
    def cast_graph_params(cls, values):
        values["graph_params"] = TYPE_PARAMS_MAP[
            values["chart_type"]
        ].parse_obj(values["graph_params"])

        return values
