from typing import Optional

import pandas as pd
from dash import dcc, html

from app.data_manager import apply_filter, get_data
from app.schema.params import AppliedFilters
from app.schema.requests import ChartBuilderRequest, FigCSSArgs
from app.services.chart_factory import ChartBuilderService
from app.services.dash_layout.controls import create_filters_control
from app.utils import check_validate_chart_config


def create_chart(
    df: pd.DataFrame,
    config_model: ChartBuilderRequest,
    applied_filters: Optional[AppliedFilters] = None,
):
    if applied_filters is not None:
        df = apply_filter(df=df, applied_filters=applied_filters)

    chart_builder = ChartBuilderService(config_model.chart_type)
    fig = chart_builder.build(
        df=df,
        chart_params=config_model.chart_params,
    )

    return fig


def create_chart_content(
    chart_name: str,
    fig_css_args: FigCSSArgs,
):
    config_model = check_validate_chart_config(chart_name)
    df = get_data(config_model.table_name)
    fig = create_chart(df=df, config_model=config_model)

    graph = html.Div(
        dcc.Graph(
            id="chart", figure=fig, style=fig_css_args.dict(exclude_none=True)
        )
    )

    filters_control = create_filters_control(
        df=df, filters=config_model.chart_params.filters
    )

    """
    HTML Pattern

    <div>
        <div>{graph}</div>
        <div>{filters}</div>
    </div>
    """
    return [graph, filters_control]


def update_chart(chart_name: str, applied_filters: AppliedFilters):
    config_model = check_validate_chart_config(chart_name)
    df = get_data(config_model.table_name)
    fig = create_chart(
        df=df, config_model=config_model, applied_filters=applied_filters
    )

    return fig
