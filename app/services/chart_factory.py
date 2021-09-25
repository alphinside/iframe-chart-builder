from http import HTTPStatus
from pathlib import Path
from typing import Type

from dash import dcc
from fastapi import HTTPException

from app.config import get_settings
from app.constant import STANDARD_CHARTS_CONFIG, ChartTypes
from app.data_manager import get_data
from app.schema.params import BaseChartParams
from app.schema.requests import ChartBuilderRequest, FigCSSArgs
from app.services.chart_builder import ChartBuilderInterface
from app.services.chart_builder.bar import BarChartBuilder
from app.services.chart_builder.choropleth_map import ChoroplethMapBuilder
from app.utils import read_config, serialize_config


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

    def dump_config(self, config: ChartBuilderRequest) -> ChartBuilderRequest:
        chart_config_dir = get_settings().charts_output_dir / Path(
            config.chart_name
        )

        serialize_config(
            config=config,
            output_dir=chart_config_dir,
            filename=STANDARD_CHARTS_CONFIG,
        )

    def build(self, table_name: str, chart_params: Type[BaseChartParams]):
        df = get_data(table_name)

        fig = self.chart_builder.build_chart(chart_params=chart_params, df=df)

        return fig


factory = ChartBuilderFactory()
factory.register_type(ChartTypes.bar, BarChartBuilder)
factory.register_type(ChartTypes.choropleth_map, ChoroplethMapBuilder)


def create_chart(chart_name: str, fig_css_args: FigCSSArgs):
    chart_config_file_path = (
        get_settings().charts_output_dir / chart_name / STANDARD_CHARTS_CONFIG
    )

    if not chart_config_file_path.exists():
        raise FileNotFoundError(
            f"config chart `{chart_name}` not found "
            f"in {chart_config_file_path}"
        )

    config_model = read_config(chart_config_file_path)

    chart_builder = ChartBuilderService(config_model.chart_type)
    fig = chart_builder.build(
        table_name=config_model.table_name,
        chart_params=config_model.chart_params,
    )

    return [dcc.Graph(figure=fig, style=fig_css_args.dict(exclude_none=True))]
