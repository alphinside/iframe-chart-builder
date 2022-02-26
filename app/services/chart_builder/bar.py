from typing import Dict, Tuple

import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from app.constant import BarOrientation, BarPercentageColumnBase
from app.schema.params import BarChartParams
from app.services.chart_builder import ChartBuilderInterface


class BarChartBuilder(ChartBuilderInterface):
    def build_chart(
        self, chart_params: BarChartParams, df: pd.DataFrame
    ) -> Figure:

        if chart_params.column_for_color is None:
            chart_params.column_for_color = chart_params.column_for_y

        bar_kwargs = {
            "x": chart_params.column_for_x,
            "y": chart_params.column_for_y,
            "title": chart_params.title,
            "color": chart_params.column_for_color,
            "color_discrete_sequence": chart_params.color_opt.discrete,
            "color_continuous_scale": chart_params.color_opt.continuous,
            "barmode": chart_params.barmode,
            "orientation": chart_params.orientation.name,
        }

        vis_df = self._merge_df_based_on_visualize_column(
            chart_params=chart_params, df=df
        )

        if isinstance(chart_params.column_for_y, list) or isinstance(
            chart_params.column_for_x, list
        ):
            bar_kwargs.pop("color")
            fig = px.bar(vis_df, **bar_kwargs)
            return fig

        vis_df, bar_kwargs = self._calculate_and_add_percentage_long_format(
            chart_params=chart_params, vis_df=vis_df, bar_kwargs=bar_kwargs
        )

        fig = px.bar(vis_df, **bar_kwargs)

        return fig

    def _calculate_and_add_percentage_long_format(
        self,
        chart_params: BarChartParams,
        vis_df: pd.DataFrame,
        bar_kwargs: Dict,
    ) -> Tuple[pd.DataFrame, Dict]:
        if chart_params.column_for_y == chart_params.column_for_color:
            if chart_params.orientation == BarOrientation.v:
                value_column = chart_params.column_for_y
            else:
                value_column = chart_params.column_for_x

            value_sum = vis_df[value_column].sum()
            vis_df["percentage"] = vis_df[value_column] / value_sum
        else:
            if (
                chart_params.percentage_column_base
                == BarPercentageColumnBase.column_for_x
            ):
                if chart_params.orientation == BarOrientation.v:
                    group_column = chart_params.column_for_x
                    value_column = chart_params.column_for_y
                else:
                    group_column = chart_params.column_for_y
                    value_column = chart_params.column_for_x
            elif (
                chart_params.percentage_column_base
                == BarPercentageColumnBase.column_for_color
            ):
                group_column = chart_params.column_for_color
                if chart_params.orientation == BarOrientation.v:
                    value_column = chart_params.column_for_y
                else:
                    value_column = chart_params.column_for_x
            else:
                raise ValueError(
                    "unknown `percentage_column_base` "
                    f"column: {chart_params.percentage_column_base}"
                )

            group_value_sum = vis_df.groupby([group_column]).sum()
            group_value_sum = group_value_sum.rename(
                columns={"count": "group_value_sum"}
            )
            vis_df = vis_df.merge(group_value_sum, on=group_column)
            vis_df["percentage"] = (
                vis_df[value_column] / vis_df["group_value_sum"]
            )
            vis_df.drop(["group_value_sum"], axis=1)

        vis_df["percentage"] = vis_df["percentage"].map(
            lambda n: "{:,.2%}".format(n)
        )

        bar_kwargs.update({"text": "percentage"})

        return (vis_df, bar_kwargs)

    def _merge_df_based_on_visualize_column(
        self, chart_params: BarChartParams, df: pd.DataFrame
    ) -> pd.DataFrame:
        vis_column_list = [
            chart_params.column_for_x,
            chart_params.column_for_y,
            chart_params.column_for_color,
        ]
        flattened_vis_column_list = []
        for columns in vis_column_list:
            if isinstance(columns, list):
                flattened_vis_column_list.extend(columns)
            else:
                flattened_vis_column_list.append(columns)

        vis_column_list = list(set(flattened_vis_column_list))

        if chart_params.orientation == BarOrientation.v:
            group_column = [chart_params.column_for_x]
        else:
            group_column = [chart_params.column_for_y]

        if chart_params.column_for_color != chart_params.column_for_y:
            group_column.append(chart_params.column_for_color)

        vis_df = (
            df[vis_column_list].groupby(by=group_column).sum().reset_index()
        )

        return vis_df
