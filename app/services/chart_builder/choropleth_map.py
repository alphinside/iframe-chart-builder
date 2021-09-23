import json
from http import HTTPStatus

import plotly.express as px
from fastapi import HTTPException
from plotly.graph_objs._figure import Figure

from app.schema.errors import COLUMN_NOT_FOUND_ERROR
from app.schema.params import ChoroplethMapParams
from app.services.chart_builder import ChartBuilderInterface

with open("app/data/indonesia-province.json", "r") as f:
    indo_geojson = json.loads(f.read())


class ChoroplethMapBuilder(ChartBuilderInterface):
    def validate_columns(self, graph_params: ChoroplethMapParams):
        columns_not_found = []

        if graph_params.column_for_province not in self.df.columns:
            columns_not_found.append(graph_params.column_for_province)

        if graph_params.column_for_color not in self.df.columns:
            columns_not_found.append(graph_params.column_for_color)

        if len(columns_not_found) != 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=COLUMN_NOT_FOUND_ERROR.format_map(
                    {"column_names": columns_not_found}
                ),
            )

    def build_chart(self, graph_params: ChoroplethMapParams) -> Figure:
        try:
            fig = px.choropleth_mapbox(
                self.df,
                geojson=indo_geojson,
                color=graph_params.column_for_color,
                locations=graph_params.column_for_province,
                featureidkey="properties.state",
                center={"lat": -4.050027, "lon": 116.375442},
                zoom=graph_params.zoom_level,
                mapbox_style="open-street-map",
                width=graph_params.width,
                height=graph_params.height,
            )

        except Exception as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e)

        return fig
