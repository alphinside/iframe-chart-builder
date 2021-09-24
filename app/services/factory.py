from http import HTTPStatus
from pathlib import Path
from typing import Type

from fastapi import HTTPException
from omegaconf.dictconfig import DictConfig

from app.config import get_settings
from app.constant import (
    CHARTS_ROUTE,
    DASH_MOUNT_ROUTE,
    STANDARD_CHARTS_CONFIG,
    ChartTypes,
)
from app.data_manager import get_data
from app.schema.params import BaseChartParams
from app.schema.requests import ChartBuilderRequest
from app.services.chart_builder import ChartBuilderInterface
from app.services.chart_builder.bar import BarChartBuilder
from app.services.chart_builder.choropleth_map import ChoroplethMapBuilder
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

    def construct_dict_config(self, params: ChartBuilderRequest) -> DictConfig:
        dict_config = DictConfig(params.dict())
        dict_config.chart_url = str(
            Path(DASH_MOUNT_ROUTE + CHARTS_ROUTE) / params.chart_name
        )

        return dict_config

    def create_and_dump_config(
        self, params: ChartBuilderRequest
    ) -> DictConfig:
        dict_config = self.construct_dict_config(params)

        chart_config_dir = get_settings().charts_output_dir / Path(
            params.chart_name
        )
        serialize_config(
            config=dict_config,
            output_dir=chart_config_dir,
            filename=STANDARD_CHARTS_CONFIG,
        )

        return dict_config

    # def build(self, filename: str, uploaded_data: bytes):
    #     df = pd.read_excel(uploaded_data)
    #     self.chart_builder.validate_columns(
    #         chart_params=self.chart_params, df=df
    #     )
    #     fig = self.chart_builder.build_chart(
    #         chart_params=self.chart_params, df=df
    #     )

    #     if self.vis_type == VisTypes.table:
    #         resource_name = Path(filename).with_suffix(".html")
    #         output_path = (
    #             get_settings().table_snippet_output_dir / resource_name
    #         )
    #         resource_path = Path(TABLES_ROUTE) / resource_name
    #     else:
    #         resource_name = Path(self.chart_name).with_suffix(".html")
    #         output_path = get_settings().charts_output_dir / resource_name
    #         resource_path = Path(CHARTS_ROUTE) / resource_name

    #     return resource_path


factory = ChartBuilderFactory()
factory.register_type(ChartTypes.bar, BarChartBuilder)
factory.register_type(ChartTypes.choropleth_map, ChoroplethMapBuilder)
