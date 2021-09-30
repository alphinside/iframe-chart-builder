from http import HTTPStatus

import pandas as pd
import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.errors import COLUMN_NOT_FOUND_ERROR
from app.schema.params import BubbleChartParams
from app.services.chart_builder import ChartBuilderInterface


class BubbleChartBuilder(ChartBuilderInterface):
    def validate_columns(
        self, chart_params: BubbleChartParams, df: pd.DataFrame
    ):
        columns_not_found = []

        if chart_params.column_for_x not in df.columns:
            columns_not_found.append(chart_params.column_for_x)

        if chart_params.column_for_y not in df.columns:
            columns_not_found.append(chart_params.column_for_y)

        if chart_params.column_for_color is not None:
            if chart_params.column_for_color not in df.columns:
                columns_not_found.append(chart_params.column_for_color)

        if chart_params.column_for_size is not None:
            if chart_params.column_for_size not in df.columns:
                columns_not_found.append(chart_params.column_for_size)

        if chart_params.column_for_hover_name is not None:
            if chart_params.column_for_hover_name not in df.columns:
                columns_not_found.append(chart_params.column_for_hover_name)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": columns_not_found}
                ),
            )

    def build_chart(
        self, chart_params: BubbleChartParams, df: pd.DataFrame
    ) -> Figure:
        fig = px.scatter(
            df,
            x=chart_params.column_for_x,
            y=chart_params.column_for_y,
            color=chart_params.column_for_color,
            size=chart_params.column_for_size,
            color_discrete_sequence=chart_params.color_opt.discrete,
            color_continuous_scale=chart_params.color_opt.continuous,
            title=chart_params.title,
            log_x=chart_params.apply_log_x,
            size_max=chart_params.bubble_size_max,
            hover_name=chart_params.column_for_hover_name,
        )

        return fig
