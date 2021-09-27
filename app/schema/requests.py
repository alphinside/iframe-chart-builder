from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, root_validator

from app.constant import ChartTypes
from app.schema.params import BarChartParams, ChoroplethMapParams

TYPE_PARAMS_MAP = {
    ChartTypes.bar: BarChartParams,
    ChartTypes.choropleth_map: ChoroplethMapParams,
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


class BaseChartBuilderRequest(BaseModel):
    table_name: str
    chart_name: str
    chart_type: ChartTypes
    chart_params: Dict[str, Any]


class BarChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: BarChartParams
    chart_type: ChartTypes = Field(ChartTypes.bar, const=True)

    class Config:
        schema_extra = {
            "example": {
                "table_name": "example_bar_chart_long",
                "chart_name": "example_bar_long",
                "chart_params": {
                    "title": "Medal Winnings",
                    "column_for_x": "nation",
                    "column_for_y": ["count"],
                    "column_for_color": "medal",
                    "filters": [
                        {"column": "medal", "type": "categorical"},
                        {"column": "count", "type": "numerical"},
                    ],
                },
            }
        }


class ChoroplethMapBuilderRequest(BaseChartBuilderRequest):
    chart_params: ChoroplethMapParams
    chart_type: ChartTypes = Field(ChartTypes.choropleth_map, const=True)

    class Config:
        schema_extra = {
            "example": {
                "table_name": "example_choropleth_map",
                "chart_name": "provinces_residents",
                "chart_params": {
                    "title": "Indonesia Population",
                    "column_for_province": "state",
                    "column_for_color": "residents",
                    "filters": [
                        {"column": "state", "type": "categorical"},
                        {"column": "residents", "type": "numerical"},
                    ],
                },
            }
        }
