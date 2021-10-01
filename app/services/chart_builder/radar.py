import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure

from app.schema.params import RadarChartParams
from app.services.chart_builder import ChartBuilderInterface


class RadarChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: RadarChartParams, df: pd.DataFrame
    ) -> Figure:

        fig = go.Figure()

        for idx, item in df.iterrows():
            item_radius = item[chart_params.column_for_theta].tolist()

            item_fig = px.line_polar(
                df,
                r=item_radius,
                theta=chart_params.column_for_theta,
                line_close=True,
            )
            item_fig.update_traces(
                overwrite=True,
                line={"color": chart_params.color_opt.discrete[idx]},
                fill=chart_params.fill,
                name=item[chart_params.column_for_radius],
                showlegend=True,
                marker={"symbol": "circle"},
            )
            fig.add_trace(item_fig.data[0])

        fig.update_layout(
            title=chart_params.title,
            legend_title_text=chart_params.column_for_radius,
            showlegend=True,
        )

        return fig
