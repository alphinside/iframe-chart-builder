from typing import Any, Dict, Optional

from pydantic import BaseModel, root_validator

from app.constant import ChartTypes
from app.schema.params import BarChartParams, ChoroplethMapParams

TYPE_PARAMS_MAP = {
    ChartTypes.bar: BarChartParams,
    ChartTypes.choropleth_map: ChoroplethMapParams,
}


class ChartBuilderRequest(BaseModel):
    table_name: str
    chart_name: str
    chart_type: ChartTypes
    chart_params: Dict[str, Any]

    @root_validator
    def cast_chart_params(cls, values):
        values["chart_params"] = TYPE_PARAMS_MAP[
            values["chart_type"]
        ].parse_obj(values["chart_params"])

        return values


class FigSize(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None

    @root_validator(pre=True)
    def cast_chart_params(cls, values):
        if "width" in values:
            values["width"] = int(values["width"][0])

        if "height" in values:
            values["height"] = int(values["height"][0])

        return values
