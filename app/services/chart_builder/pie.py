import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.schema.params import PieChartParams
from app.services.chart_builder import ChartBuilderInterface


class PieChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: PieChartParams, df: pd.DataFrame
    ) -> Figure:
        fig = px.pie(
            df,
            values=chart_params.column_for_values,
            names=chart_params.column_for_names,
            color_discrete_sequence=chart_params.color_opt.discrete,
            title=chart_params.title,
            hole=chart_params.center_hole_ratio,
        )

        return fig
