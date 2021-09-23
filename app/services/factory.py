from http import HTTPStatus
from pathlib import Path
from typing import Type

import pandas as pd
from fastapi import HTTPException

from app.config import get_settings
from app.constant import CHARTS_ROUTE, TABLES_ROUTE, VisTypes
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

    def get_creator(self, type: VisTypes):
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
        self.chart_name = params.chart_name
        self.vis_type = params.vis_type
        self.chart_params = params.chart_params

    def build(self, filename: str, uploaded_data: bytes):
        df = pd.read_excel(uploaded_data)
        self.chart_builder.validate_columns(
            chart_params=self.chart_params, df=df
        )
        fig = self.chart_builder.build_chart(
            chart_params=self.chart_params, df=df
        )

        if self.vis_type == VisTypes.table:
            resource_name = Path(filename).with_suffix(".html")
            output_path = (
                get_settings().table_snippet_output_dir / resource_name
            )
            resource_path = Path(TABLES_ROUTE) / resource_name
        else:
            resource_name = Path(self.chart_name).with_suffix(".html")
            output_path = get_settings().charts_output_dir / resource_name
            resource_path = Path(CHARTS_ROUTE) / resource_name

        self.chart_builder.dump_to_html(fig=fig, output_path=output_path)

        return resource_path


factory = ChartBuilderFactory()
factory.register_type(VisTypes.bar, BarChartBuilder)
factory.register_type(VisTypes.choropleth_map, ChoroplethMapBuilder)
