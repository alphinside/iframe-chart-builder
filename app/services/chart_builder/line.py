import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import LineChartParams
from app.services.chart_builder import ChartBuilderInterface


class LineChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: LineChartParams, df: pd.DataFrame
    ) -> Figure:
        fig = px.line(
            df,
            x=chart_params.column_for_x,
            y=chart_params.column_for_y,
            color=chart_params.column_for_color,
            color_discrete_sequence=chart_params.color_opt.discrete,
            title=chart_params.title,
        )

        return fig
