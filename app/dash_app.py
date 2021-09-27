import logging
from http import HTTPStatus

import config
import dash
from dash import dcc, html
from dash.dependencies import ALL, MATCH, Input, Output, State
from flask import Response

from app.constant import (
    COLUMN_FILTER_CAT,
    COLUMN_FILTER_NUM,
    COLUMN_FILTER_SELECT_ALL,
    DASH_ROOT_ROUTE,
    SELECT_ALL_VALUE,
)
from app.schema.params import AppliedFilters, CategoricalFilterState
from app.services.dash_layout.chart import create_chart_content, update_chart
from app.services.dash_layout.table import create_table_snippet

dash_app = dash.Dash(__name__, requests_pathname_prefix=DASH_ROOT_ROUTE)

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@dash_app.callback(
    output=Output({"type": COLUMN_FILTER_SELECT_ALL, "index": MATCH}, "value"),
    inputs={
        "selected_fields": Input(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "value"
        ),
        "all_options": State(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "options"
        ),
    },
)
def select_all_cat_activation(selected_fields, all_options):
    if selected_fields is not None and len(selected_fields) == len(
        all_options
    ):
        return [SELECT_ALL_VALUE]

    return []


@dash_app.callback(
    output=Output({"type": COLUMN_FILTER_CAT, "index": MATCH}, "value"),
    inputs={
        "selected_fields": Input(
            {"type": COLUMN_FILTER_SELECT_ALL, "index": MATCH}, "value"
        ),
        "all_options": State(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "options"
        ),
        "active_state": State(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "value"
        ),
    },
)
def link_select_all_to_multi_select(
    selected_fields, all_options, active_state
):
    if selected_fields == [SELECT_ALL_VALUE]:
        return [option["value"] for option in all_options]

    return active_state


@dash_app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_initial_page(pathname):
    try:
        if pathname.startswith("/dash/charts"):
            if pathname in config.charts:
                return create_chart_content(chart_name=config.charts[pathname])

        if pathname.startswith("/dash/tables"):
            if pathname in config.table_snippets:
                return create_table_snippet(
                    table_name=config.table_snippets[pathname]
                )

        Response("404 Not Found", HTTPStatus.NOT_FOUND)
        return [html.H1("404 Not Found")]

    except Exception as e:
        Response(
            f"500 Internal Server Error : {e}",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return [html.H1(f"500 Internal Server Error : {e}")]


@dash_app.callback(
    output=Output("chart", "figure"),
    inputs={
        "cat_values": Input(
            {"type": COLUMN_FILTER_CAT, "index": ALL}, "value"
        ),
        "num_values": Input(
            {"type": COLUMN_FILTER_NUM, "index": ALL}, "value"
        ),
        "cat_options": State(
            {"type": COLUMN_FILTER_CAT, "index": ALL}, "options"
        ),
        "cat_id": State({"type": COLUMN_FILTER_CAT, "index": ALL}, "id"),
        "num_options": State(
            {"type": COLUMN_FILTER_NUM, "index": ALL}, "options"
        ),
        "num_id": State({"type": COLUMN_FILTER_NUM, "index": ALL}, "id"),
        "pathname": State("url", "pathname"),
        "current_fig": State("chart", "figure"),
    },
)
def update_chart_based_on_filter(
    cat_values,
    num_values,
    cat_options,
    num_options,
    cat_id,
    num_id,
    pathname,
    current_fig,
):
    ctx = dash.callback_context

    if not ctx.triggered:
        return current_fig

    applied_filters = _build_filters(
        cat_values, num_values, cat_options, num_options, cat_id, num_id
    )

    try:
        updated_fig = update_chart(
            chart_name=config.charts[pathname],
            applied_filters=applied_filters,
        )

        return updated_fig
    except Exception as e:
        logging.error(e)
        return current_fig


# TODO handle numerical
def _build_filters(
    cat_values, num_values, cat_options, num_options, cat_id, num_id
) -> AppliedFilters:
    cat_filters = []

    for values, options, column in zip(cat_values, cat_options, cat_id):
        if values is None or len(values) == 0 or len(values) == len(options):
            continue

        filter = CategoricalFilterState(column=column["index"], values=values)
        cat_filters.append(filter)

    return AppliedFilters(categorical=cat_filters)
