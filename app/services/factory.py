from http import HTTPStatus
from pathlib import Path, PosixPath
from typing import Type

import pandas as pd
from fastapi import HTTPException
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig

from app.config import get_settings
from app.constant import (
    CHARTS_ROUTE,
    DASH_MOUNT_ROUTE,
    STANDARD_CHARTS_CONFIG,
    TABLES_ROUTE,
    VisTypes,
)
from app.schema.requests import ChartBuilderRequest
from app.services.chart_builder import ChartBuilderInterface
from app.services.chart_builder.bar import BarChartBuilder
from app.services.chart_builder.choropleth_map import ChoroplethMapBuilder


class ChartBuilderFactory:
    def __init__(self):
        self._creators = {}

    def register_type(
        self,
        type: VisTypes,
        creator: Type[ChartBuilderInterface],
    ):
        assert issubclass(creator, ChartBuilderInterface)
        self._creators[type] = creator

    def get_creator(self, type: VisTypes) -> Type[ChartBuilderInterface]:
        creator = self._creators.get(type)
        if not creator:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"vis type {type} is not supported",
            )

        return creator


class ChartBuilderService:
    def __init__(self, params: ChartBuilderRequest):
        creator = factory.get_creator(params.vis_type)
        self.chart_builder = creator()
        self.params = params
        # self.chart_name = params.chart_name
        # self.vis_type = params.vis_type
        # self.chart_params = params.chart_params

    @staticmethod
    def _create_and_serialize_config(
        config: DictConfig, output_path: PosixPath
    ):

        OmegaConf.save(config=config, f=output_path / STANDARD_CHARTS_CONFIG)

    def construct_dict_config(self) -> DictConfig:
        dict_config = DictConfig(self.params.dict())
        dict_config.chart_url = (
            Path(DASH_MOUNT_ROUTE)
            / Path(CHARTS_ROUTE)
            / self.params.chart_name
        )
        dict_config.table_url = (
            Path(DASH_MOUNT_ROUTE)
            / Path(TABLES_ROUTE)
            / self.params.chart_name
        )

        return dict_config

    def eval_and_dump_config(self, filename: str, uploaded_data: bytes):
        df = pd.read_excel(uploaded_data)

        self.chart_builder.validate_columns(
            chart_params=self.params.chart_params, df=df
        )

        chart_config_dir = get_settings().charts_output_dir / Path(
            self.params.chart_name
        )
        chart_config_dir.mkdir(exist_ok=True)

        serialized_data_path = chart_config_dir / Path(filename)
        self._serialize_data(df=df, output_path=serialized_data_path)

        dict_config = self.construct_dict_config()

        self._create_and_serialize_config(
            config=dict_config, output_path=chart_config_dir
        )

        # self.chart_builder.dump_config(params)

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
factory.register_type(VisTypes.bar, BarChartBuilder)
factory.register_type(VisTypes.choropleth_map, ChoroplethMapBuilder)
