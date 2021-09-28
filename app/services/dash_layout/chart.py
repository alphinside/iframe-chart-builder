from typing import Optional, Type

import pandas as pd
from dash import dcc, html

from app.constant import ResourceType
from app.data_manager import apply_filter, get_data
from app.schema.params import AppliedFilters
from app.schema.requests import BaseChartBuilderRequest
from app.services.chart_factory import ChartBuilderService
from app.services.dash_layout.controls import create_filters_control
from app.utils import check_validate_chart_config, check_validate_style_config


def create_chart(
    df: pd.DataFrame,
    config_model: Type[BaseChartBuilderRequest],
    applied_filters: Optional[AppliedFilters] = None,
):
    if applied_filters is not None:
        df = apply_filter(df=df, applied_filters=applied_filters)

    chart_builder = ChartBuilderService(config_model.chart_type)
    fig = chart_builder.build(
        df=df,
        chart_params=config_model.chart_params,
    )
    fig.update_layout(
        autosize=True,
    )
    fig.update_yaxes(automargin=True)

    return fig


def create_chart_content(
    chart_name: str,
):
    config_model = check_validate_chart_config(chart_name)
    df = get_data(config_model.table_name)
    fig = create_chart(df=df, config_model=config_model)

    style = check_validate_style_config(
        name=chart_name, resource=ResourceType.chart
    )

    graph = dcc.Graph(id="chart", figure=fig, style=style.figure)

    filters_control = create_filters_control(
        df=df,
        filters=config_model.chart_params.filters,
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


def update_chart(chart_name: str, applied_filters: AppliedFilters):
    config_model = check_validate_chart_config(chart_name)
    df = get_data(config_model.table_name)
    fig = create_chart(
        df=df, config_model=config_model, applied_filters=applied_filters
    )

    return fig
