from typing import Type

from app.constant import ChartTypes
from app.schema.requests import ChartBuilderRequest
from app.services.chart_builder import ChartBuilderInterface
from app.services.chart_builder.bar import BarChartBuilder
from app.services.chart_builder.choropleth_map import ChoroplethMapBuilder


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

    def get_creator(self, type: ChartTypes):
        creator = self._creators.get(type)
        if not creator:
            raise ValueError(
                f"chart builder for '{type}' chart type is not exist"
            )

        return creator


class ChartBuilderService:
    def __init__(self, params: ChartBuilderRequest):
        creator = factory.get_creator(params.chart_type)
        self.chart_builder = creator(
            input_path=params.input_path, output_path=params.output_path
        )
        self.graph_params = params.graph_params

    def build(self):
        self.chart_builder.validate_columns(self.graph_params)
        fig = self.chart_builder.build_chart(self.graph_params)
        self.chart_builder.dump_to_html(fig)


factory = ChartBuilderFactory()
factory.register_type(ChartTypes.bar, BarChartBuilder)
factory.register_type(ChartTypes.choropleth_map, ChoroplethMapBuilder)
