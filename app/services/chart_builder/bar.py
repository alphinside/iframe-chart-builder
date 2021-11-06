import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.constant import BarOrientation
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
            "orientation": chart_params.orientation.name,
        }

        if isinstance(chart_params.column_for_y, list):
            kwargs.pop("color")

        if chart_params.column_for_color is not None:
            if chart_params.orientation == BarOrientation.v:
                group_column = chart_params.column_for_x
                value_column = chart_params.column_for_y
            else:
                group_column = chart_params.column_for_y
                value_column = chart_params.column_for_x

            color_value_sum = df.groupby([group_column]).sum()
            color_value_sum = color_value_sum.rename(
                columns={"count": "color_value_sum"}
            )
            df = df.merge(color_value_sum, on=group_column)
            df["percentage"] = df[value_column] / df["color_value_sum"]
            df["percentage"] = (
                df["percentage"]
                .round(decimals=2)
                .map(lambda n: "{:,.2%}".format(n))
            )

            kwargs.update({"text": "percentage"})

        fig = px.bar(df, **kwargs)

        return fig
