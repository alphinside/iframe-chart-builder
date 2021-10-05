import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import BarChartParams
from app.services.chart_builder import ChartBuilderInterface


class BarChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: BarChartParams, df: pd.DataFrame
    ) -> Figure:

        kwargs = {
            "x": chart_params.column_for_x,
            "y": chart_params.column_for_y,
            "title": chart_params.title,
            "color": chart_params.column_for_color,
            "color_discrete_sequence": chart_params.color_opt.discrete,
            "color_continuous_scale": chart_params.color_opt.continuous,
            "barmode": chart_params.barmode,
        }

        if isinstance(chart_params.column_for_y, list):
            kwargs.pop("color")

        fig = px.bar(df, **kwargs)

        return fig
