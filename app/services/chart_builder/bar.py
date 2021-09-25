from http import HTTPStatus

import pandas as pd
import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.errors import COLUMN_NOT_FOUND_ERROR
from app.schema.params import BarChartParams
from app.services.chart_builder import ChartBuilderInterface


class BarChartBuilder(ChartBuilderInterface):
    def validate_columns(self, chart_params: BarChartParams, df: pd.DataFrame):
        columns_not_found = []

        if chart_params.column_for_x not in df.columns:
            columns_not_found.append(chart_params.column_for_x)

        if isinstance(chart_params.column_for_x, str):
            y_columns = [chart_params.column_for_x]
        else:
            y_columns = chart_params.column_for_x

        for column in y_columns:
            if column not in df.columns:
                columns_not_found.append(column)

        if chart_params.column_for_color is not None:
            if chart_params.column_for_color not in df.columns:
                columns_not_found.append(column)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": columns_not_found}
                ),
            )

    def build_chart(
        self, chart_params: BarChartParams, df: pd.DataFrame
    ) -> Figure:

        if isinstance(chart_params.column_for_y, list):
            fig = px.bar(
                df,
                x=chart_params.column_for_x,
                y=chart_params.column_for_y,
                title=chart_params.title,
            )
        else:
            fig = px.bar(
                df,
                x=chart_params.column_for_x,
                y=chart_params.column_for_y,
                color=chart_params.column_for_color,
                title=chart_params.title,
            )

        return fig
