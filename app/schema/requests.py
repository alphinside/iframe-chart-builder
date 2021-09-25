from typing import Any, Dict

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
    chart_url: str = ""

    @root_validator
    def cast_chart_params_and_set_default(cls, values):
        values["chart_params"] = TYPE_PARAMS_MAP[
            values["chart_type"]
        ].parse_obj(values["chart_params"])

        return values


class FigSize(BaseModel):
    width: int = 1280
    height: int = 720

    @root_validator(pre=True)
    def cast_chart_params(cls, values):
        if "width" in values:
            values["width"] = int(values["width"][0])

        if "height" in values:
            values["height"] = int(values["height"][0])

        return values
