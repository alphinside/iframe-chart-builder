from http import HTTPStatus

import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.schema.errors import COLUMN_NOT_FOUND_ERROR
from app.schema.params import BarChartParams
from app.services.chart_builder import ChartBuilderInterface


class BarChartBuilder(ChartBuilderInterface):
    def validate_columns(self, graph_params: BarChartParams):
        columns_not_found = []

        if graph_params.column_for_x not in self.df.columns:
            columns_not_found.append(graph_params.column_for_x)

        if isinstance(graph_params.column_for_x, str):
            y_columns = [graph_params.column_for_x]
        else:
            y_columns = graph_params.column_for_x

        for column in y_columns:
            if column not in self.df.columns:
                columns_not_found.append(column)

        if graph_params.column_for_color is not None:
            if graph_params.column_for_color not in self.df.columns:
                columns_not_found.append(column)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": columns_not_found}
                ),
            )

    def build_chart(self, graph_params: BarChartParams) -> Figure:
        try:
            if isinstance(graph_params.column_for_y, list):
                fig = px.bar(
                    self.df,
                    x=graph_params.column_for_x,
                    y=graph_params.column_for_y,
                    title=graph_params.title,
                    width=graph_params.width,
                    height=graph_params.height,
                )
            else:
                fig = px.bar(
                    self.df,
                    x=graph_params.column_for_x,
                    y=graph_params.column_for_y,
                    color=graph_params.column_for_color,
                    title=graph_params.title,
                    width=graph_params.width,
                    height=graph_params.height,
                )
        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e)

        return fig
