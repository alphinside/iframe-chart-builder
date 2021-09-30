import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import BubbleChartParams
from app.services.chart_builder import ChartBuilderInterface


class BubbleChartBuilder(ChartBuilderInterface):
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
