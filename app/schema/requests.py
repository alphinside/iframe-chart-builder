from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.constant import ChartTypes
from app.schema.params import (
    BarChartParams,
    BubbleChartParams,
    BubbleMapParams,
    ChoroplethMapParams,
    LineChartParams,
    PieChartParams,
    RadarChartParams,
    SunburstChartParams,
    WindroseChartParams,
)

TYPE_PARAMS_MAP = {
    ChartTypes.bar: BarChartParams,
    ChartTypes.choropleth_map: ChoroplethMapParams,
    ChartTypes.bubble_map: BubbleMapParams,
    ChartTypes.bubble: BubbleChartParams,
    ChartTypes.line: LineChartParams,
    ChartTypes.pie: PieChartParams,
    ChartTypes.windrose: WindroseChartParams,
    ChartTypes.sunburst: SunburstChartParams,
    ChartTypes.radar: RadarChartParams,
}

StyleDict = Dict[str, Any]


class ChartStyle(BaseModel):
    figure: Optional[StyleDict] = {}
    filters_group: Optional[StyleDict] = {}
    filters_entity: Optional[StyleDict] = {}
    table: Optional[StyleDict] = {}

    class Config:
        schema_extra = {
            "figure": {
                "height": "50vh",
                "width": "100vh",
                "display": "inline-block",
            },
            "filters_group": {
                "height": "50vh",
                "width": "20vh",
                "display": "inline-block",
                "vertical-align": "top",
            },
            "filters_entity": {},
        }


class BaseChartBuilderRequest(BaseModel):
    table_name: str
    chart_name: str
    chart_type: ChartTypes
    chart_params: Dict[str, Any]


class BarChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: BarChartParams
    chart_type: ChartTypes = Field(ChartTypes.bar, const=True)


class ChoroplethMapBuilderRequest(BaseChartBuilderRequest):
    chart_params: ChoroplethMapParams
    chart_type: ChartTypes = Field(ChartTypes.choropleth_map, const=True)


class BubbleMapBuilderRequest(BaseChartBuilderRequest):
    chart_params: BubbleMapParams
    chart_type: ChartTypes = Field(ChartTypes.bubble_map, const=True)


class BubbleChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: BubbleChartParams
    chart_type: ChartTypes = Field(ChartTypes.bubble, const=True)


class LineChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: LineChartParams
    chart_type: ChartTypes = Field(ChartTypes.line, const=True)


class PieChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: PieChartParams
    chart_type: ChartTypes = Field(ChartTypes.pie, const=True)


class WindroseChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: WindroseChartParams
    chart_type: ChartTypes = Field(ChartTypes.windrose, const=True)


class SunburstChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: SunburstChartParams
    chart_type: ChartTypes = Field(ChartTypes.sunburst, const=True)


class RadarChartBuilderRequest(BaseChartBuilderRequest):
    chart_params: RadarChartParams
    chart_type: ChartTypes = Field(ChartTypes.radar, const=True)
