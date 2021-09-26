from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, root_validator

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
    def cast_chart_params_and_set_default(cls, values):
        values["chart_params"] = TYPE_PARAMS_MAP[
            values["chart_type"]
        ].parse_obj(values["chart_params"])

        return values

    class Config:
        schema_extra = {
            "example": {
                "table_name": "example_bar_chart_long",
                "chart_name": "example_bar_long",
                "chart_type": "bar",
                "chart_params": {
                    "title": "Medal Winnings",
                    "column_for_x": "nation",
                    "column_for_y": "count",
                    "column_for_color": "medal",
                    "filters": [
                        {"column": "medal", "type": "categorical"},
                        {"column": "count", "type": "numerical"},
                    ],
                },
            },
            "all_chart_params": {
                k: v.schema_json(indent=2) for k, v in TYPE_PARAMS_MAP.items()
            },
        }


class FigCSSArgs(BaseModel):
    width: Optional[str] = Field(None, alias="figWidth")
    height: Optional[str] = Field(None, alias="figHeight")

    @root_validator(pre=True)
    def cast_chart_params(cls, values):
        if "figWidth" in values:
            values["figWidth"] = values["figWidth"][0]

        if "figHeight" in values:
            values["figHeight"] = values["figHeight"][0]

        return values
