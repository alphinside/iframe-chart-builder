from http import HTTPStatus

import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.schema.errors import COLUMN_NOT_FOUND_ERROR
from app.services.chart_builder import ChartBuilderInterface


class BarChartBuilder(ChartBuilderInterface):
    def validate_columns(self):
        columns_not_found = []

        if self.graph_params.column_for_x not in self.df.columns:
            columns_not_found.append(self.graph_params.column_for_x)

        if isinstance(self.graph_params.column_for_x, str):
            y_columns = [self.graph_params.column_for_x]
        else:
            y_columns = self.graph_params.column_for_x

        for column in y_columns:
            if column not in self.df.columns:
                columns_not_found.append(column)

        if self.graph_params.column_for_color is not None:
            if self.graph_params.column_for_color not in self.df.columns:
                columns_not_found.append(column)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": self.graph_params.column_for_x}
                ),
            )

    def build_chart(self) -> Figure:
        if isinstance(self.graph_params.column_for_y, list):
            fig = px.bar(
                self.df,
                x=self.graph_params.column_for_x,
                y=self.graph_params.column_for_y,
                title=self.title,
            )
        else:
            fig = px.bar(
                self.df,
                x=self.graph_params.column_for_x,
                y=self.graph_params.column_for_y,
                color=self.graph_params.column_for_color,
                title=self.title,
            )

        return fig
