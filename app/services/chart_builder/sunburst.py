import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import SunburstChartParams
from app.services.chart_builder import ChartBuilderInterface


class SunburstChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: SunburstChartParams, df: pd.DataFrame
    ) -> Figure:
        fig = px.sunburst(
            df,
            path=chart_params.column_for_path,
            values=chart_params.column_for_values,
            color=chart_params.column_for_color,
            color_discrete_sequence=chart_params.color_opt.discrete,
            color_continuous_scale=chart_params.color_opt.continuous,
            title=chart_params.title,
        )

        return fig
