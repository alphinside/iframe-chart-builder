from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.constant import ChartTypes
from app.schema.params import (
    BarChartParams,
    BubbleMapParams,
    ChoroplethMapParams,
)

TYPE_PARAMS_MAP = {
    ChartTypes.bar: BarChartParams,
    ChartTypes.choropleth_map: ChoroplethMapParams,
    ChartTypes.bubble_map: BubbleMapParams,
}

StyleDict = Dict[str, Any]


class ChartStyle(BaseModel):
    figure: Optional[StyleDict] = {}
    filters_group: Optional[StyleDict] = {}
    filters_entity: Optional[StyleDict] = {}
    table: Optional[StyleDict] = {}


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
                "table_name": "example_bar_long",
                "chart_name": "example_bar_long",
                "chart_params": {
                    "title": "Medal Winnings",
                    "color_opt": {
                        "discrete": {
                            "group": "qualitative",
                            "color_name": "prism",
                        },
                        "continuous": {
                            "group": "sequential",
                            "color_name": "rainbow",
                        },
                    },
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
                "chart_name": "example_choropleth_map",
                "chart_params": {
                    "title": "Indonesia Population",
                    "color_opt": {
                        "discrete": {
                            "group": "qualitative",
                            "color_name": "prism",
                        },
                        "continuous": {
                            "group": "sequential",
                            "color_name": "rainbow",
                        },
                    },
                    "column_for_location": "state",
                    "column_for_color": "residents",
                    "filters": [
                        {"column": "state", "type": "categorical"},
                        {"column": "residents", "type": "numerical"},
                    ],
                },
            }
        }


class BubbleMapBuilderRequest(BaseChartBuilderRequest):
    chart_params: BubbleMapParams
    chart_type: ChartTypes = Field(ChartTypes.bubble_map, const=True)

    class Config:
        schema_extra = {
            "example": {
                "table_name": "example_bubble_map",
                "chart_name": "example_bubble_map",
                "chart_params": {
                    "title": "Indonesia Population",
                    "color_opt": {
                        "discrete": {
                            "group": "qualitative",
                            "color_name": "prism",
                        },
                        "continuous": {
                            "group": "sequential",
                            "color_name": "rainbow",
                        },
                    },
                    "column_for_latitude": "latitude",
                    "column_for_longitude": "longitude",
                    "column_for_color": "name",
                    "column_for_size": "residents",
                    "filters": [
                        {"column": "name", "type": "categorical"},
                        {"column": "residents", "type": "numerical"},
                    ],
                },
            }
        }
