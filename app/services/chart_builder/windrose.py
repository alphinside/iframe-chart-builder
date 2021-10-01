import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import WindroseChartParams
from app.services.chart_builder import ChartBuilderInterface


class WindroseChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: WindroseChartParams, df: pd.DataFrame
    ) -> Figure:
        fig = px.bar_polar(
            df,
            r=chart_params.column_for_radius,
            theta=chart_params.column_for_theta,
            color=chart_params.column_for_color,
            color_discrete_sequence=chart_params.color_opt.discrete,
            color_continuous_scale=chart_params.color_opt.continuous,
            title=chart_params.title,
        )

        return fig
