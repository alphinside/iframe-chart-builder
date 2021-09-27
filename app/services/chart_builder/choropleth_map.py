import json
from http import HTTPStatus

import pandas as pd
import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.errors import COLUMN_NOT_FOUND_ERROR
from app.schema.params import ChoroplethMapParams
from app.services.chart_builder import ChartBuilderInterface

with open("app/data/indonesia-province.json", "r") as f:
    indo_geojson = json.loads(f.read())


class ChoroplethMapBuilder(ChartBuilderInterface):
    def validate_columns(
        self, chart_params: ChoroplethMapParams, df: pd.DataFrame
    ):
        columns_not_found = []

        if chart_params.column_for_province not in df.columns:
            columns_not_found.append(chart_params.column_for_province)

        if chart_params.column_for_color not in df.columns:
            columns_not_found.append(chart_params.column_for_color)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": columns_not_found}
                ),
            )

    def build_chart(
        self, chart_params: ChoroplethMapParams, df: pd.DataFrame
    ) -> Figure:

        fig = px.choropleth_mapbox(
            df,
            geojson=indo_geojson,
            color=chart_params.column_for_color,
            locations=chart_params.column_for_province,
            featureidkey="properties.state",
            center={"lat": -4.050027, "lon": 116.375442},
            zoom=chart_params.zoom_level,
            mapbox_style="open-street-map",
            color_continuous_scale=px.colors.sequential.Plasma_r,
        )

        return fig
