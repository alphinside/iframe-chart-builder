from http import HTTPStatus
from pathlib import Path
from typing import Optional, Type

import pandas as pd
from fastapi import HTTPException

from app.config import get_settings
from app.constant import (
    STANDARD_CHARTS_CONFIG,
    STANDARD_STYLE_CONFIG,
    ChartTypes,
)
from app.data_manager import apply_filter, get_data
from app.schema.params import AppliedFilters, BaseChartParams
from app.schema.requests import BaseChartBuilderRequest
from app.services.chart_builder import ChartBuilderInterface
from app.services.chart_builder.bar import BarChartBuilder
from app.services.chart_builder.bubble import BubbleChartBuilder
from app.services.chart_builder.bubble_map import BubbleMapBuilder
from app.services.chart_builder.choropleth_map import ChoroplethMapBuilder
from app.services.chart_builder.line import LineChartBuilder
from app.services.chart_builder.pie import PieChartBuilder
from app.services.chart_builder.radar import RadarChartBuilder
from app.services.chart_builder.sunburst import SunburstChartBuilder
from app.services.chart_builder.windrose import WindroseChartBuilder
from app.services.dash_layout.chart import create_default_chart_style
from app.utils import serialize_config


class ChartBuilderFactory:
    def __init__(self):
        self._creators = {}

    def register_type(
        self,
        type: ChartTypes,
        creator: Type[ChartBuilderInterface],
    ):
        assert issubclass(creator, ChartBuilderInterface)
        self._creators[type] = creator

    def get_creator(self, type: ChartTypes) -> Type[ChartBuilderInterface]:
        creator = self._creators.get(type)
        if not creator:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"chart type {type} is not supported",
            )

        return creator


class ChartBuilderService:
    def __init__(self, chart_type: ChartTypes):
        creator = factory.get_creator(chart_type)
        self.chart_builder = creator()

    def load_and_evaluate_data(
        self, table_name: str, chart_params: BaseChartParams
    ):
        df = get_data(table_name)
        self.chart_builder.validate_columns(df=df, chart_params=chart_params)
        self.chart_builder.validate_filters(
            df=df, filters=chart_params.filters
        )

    def dump_config(self, config: Type[BaseChartBuilderRequest]):
        chart_config_dir = get_settings().charts_output_dir / Path(
            config.chart_name
        )

        serialize_config(
            config=config,
            output_dir=chart_config_dir,
            filename=STANDARD_CHARTS_CONFIG,
        )

        chart_default_style = create_default_chart_style()

        serialize_config(
            config=chart_default_style,
            output_dir=chart_config_dir,
            filename=STANDARD_STYLE_CONFIG,
        )

    def build(self, df: pd.DataFrame, chart_params: Type[BaseChartParams]):
        fig = self.chart_builder.build_chart(chart_params=chart_params, df=df)

        return fig


factory = ChartBuilderFactory()
factory.register_type(ChartTypes.bar, BarChartBuilder)
factory.register_type(ChartTypes.choropleth_map, ChoroplethMapBuilder)
factory.register_type(ChartTypes.bubble_map, BubbleMapBuilder)
factory.register_type(ChartTypes.bubble, BubbleChartBuilder)
factory.register_type(ChartTypes.line, LineChartBuilder)
factory.register_type(ChartTypes.pie, PieChartBuilder)
factory.register_type(ChartTypes.windrose, WindroseChartBuilder)
factory.register_type(ChartTypes.sunburst, SunburstChartBuilder)
factory.register_type(ChartTypes.radar, RadarChartBuilder)


def create_chart(
    df: pd.DataFrame,
    config_model: BaseChartBuilderRequest,
    applied_filters: Optional[AppliedFilters] = None,
):

    if applied_filters is not None:
        df = apply_filter(df=df, applied_filters=applied_filters)

    chart_builder = ChartBuilderService(config_model.chart_type)
    fig = chart_builder.build(
        df=df,
        chart_params=config_model.chart_params,
    )

    fig.update_layout(template="simple_white")

    return fig
