from http import HTTPStatus

import pandas as pd
import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.errors import COLUMN_NOT_FOUND_ERROR
from app.schema.params import BubbleMapParams
from app.services.chart_builder import ChartBuilderInterface


class BubbleMapBuilder(ChartBuilderInterface):
    def validate_columns(
        self, chart_params: BubbleMapParams, df: pd.DataFrame
    ):
        columns_not_found = []

        if chart_params.column_for_latitude not in df.columns:
            columns_not_found.append(chart_params.column_for_latitude)

        if chart_params.column_for_longitude not in df.columns:
            columns_not_found.append(chart_params.column_for_longitude)

        if chart_params.column_for_color not in df.columns:
            columns_not_found.append(chart_params.column_for_color)

        if chart_params.column_for_size not in df.columns:
            columns_not_found.append(chart_params.column_for_size)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": columns_not_found}
                ),
            )

    def build_chart(
        self, chart_params: BubbleMapParams, df: pd.DataFrame
    ) -> Figure:
        fig = px.scatter_mapbox(
            df,
            lat=chart_params.column_for_latitude,
            lon=chart_params.column_for_longitude,
            color=chart_params.column_for_color,
            center={"lat": -4.050027, "lon": 116.375442},
            size=chart_params.column_for_size,
            zoom=chart_params.zoom_level,
            color_continuous_scale=px.colors.sequential.Plasma_r,
            title=chart_params.title,
            mapbox_style="open-street-map",
        )

        return fig
