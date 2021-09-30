import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import BubbleMapParams
from app.services.chart_builder import ChartBuilderInterface


class BubbleMapBuilder(ChartBuilderInterface):
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
            color_discrete_sequence=chart_params.color_opt.discrete,
            color_continuous_scale=chart_params.color_opt.continuous,
            title=chart_params.title,
            mapbox_style="open-street-map",
        )

        return fig
