from typing import List

import pandas as pd
from dash import dcc, html
from plotly.graph_objs._figure import Figure

from app.constant import ResourceType
from app.schema.params import ColumnFilter
from app.schema.requests import ChartStyle
from app.services.dash_layout.controls import create_filters_control
from app.utils import check_validate_style_config


def create_chart_content(
    chart_name: str,
    df: pd.DataFrame,
    fig: Figure,
    filters: List[ColumnFilter],
):

    style = check_validate_style_config(
        name=chart_name, resource=ResourceType.chart
    )

    fig.update_layout(
        autosize=True,
    )
    fig.update_yaxes(automargin=True)

    graph = dcc.Graph(id="chart", figure=fig, style=style.figure)

    filters_control = create_filters_control(
        df=df,
        filters=filters,
        group_style=style.filters_group,
        entity_style=style.filters_entity,
    )

    """
    HTML Pattern

    <div>
        <div>{graph}</div>
        <div>{filters}</div>
    </div>
    """
    return html.Div([graph, filters_control])


def create_default_chart_style():
    return ChartStyle(
        figure={"height": "50vh", "width": "100vh", "display": "inline-block"},
        filters_group={
            "height": "50vh",
            "width": "20vh",
            "display": "inline-block",
            "vertical-align": "top",
        },
        filters_entity={},
    )
