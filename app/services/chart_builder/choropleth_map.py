import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.config import get_settings
from app.schema.params import ChoroplethMapParams
from app.services.chart_builder import ChartBuilderInterface


class ChoroplethMapBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: ChoroplethMapParams, df: pd.DataFrame
    ) -> Figure:

        fig = px.choropleth_mapbox(
            df,
            geojson=get_settings().indo_province_geojson,
            color=chart_params.column_for_color,
            locations=chart_params.column_for_location,
            featureidkey="properties.state",
            center={"lat": -4.050027, "lon": 116.375442},
            zoom=chart_params.zoom_level,
            mapbox_style="open-street-map",
            color_discrete_sequence=chart_params.color_opt.discrete,
            color_continuous_scale=chart_params.color_opt.continuous,
            title=chart_params.title,
        )

        return fig
