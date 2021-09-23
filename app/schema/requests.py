from typing import Union

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
    chart_params: Union[BarChartParams, ChoroplethMapParams]

    @root_validator(pre=True)
    def cast_chart_params(cls, values):
        values["chart_params"] = TYPE_PARAMS_MAP[values["vis_type"]].parse_obj(
            values["chart_params"]
        )

        return values
