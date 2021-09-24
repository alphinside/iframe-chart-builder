from typing import Any, Dict

from pydantic import BaseModel, root_validator

from app.constant import VisTypes
from app.schema.params import BarChartParams, ChoroplethMapParams

TYPE_PARAMS_MAP = {
    VisTypes.bar: BarChartParams,
    VisTypes.choropleth_map: ChoroplethMapParams,
}


class ChartBuilderRequest(BaseModel):
    chart_name: str
    vis_type: VisTypes
    chart_params: Dict[str, Any]

    @root_validator
    def cast_chart_params(cls, values):
        values["chart_params"] = TYPE_PARAMS_MAP[values["vis_type"]].parse_obj(
            values["chart_params"]
        )

        return values
