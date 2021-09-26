from http import HTTPStatus
from urllib.parse import parse_qs

import config
import dash
from dash import dcc, html
from dash.dependencies import MATCH, Input, Output, State
from flask import Response

from app.constant import (
    COLUMN_FILTER_CAT,
    COLUMN_FILTER_SELECT_ALL,
    DASH_ROOT_ROUTE,
    SELECT_ALL_VALUE,
)
from app.schema.requests import FigCSSArgs
from app.services.chart_factory import create_chart
from app.services.table import create_table_snippet

dash_app = dash.Dash(__name__, requests_pathname_prefix=DASH_ROOT_ROUTE)

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@dash_app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"), Input("url", "search")],
)
def display_page(pathname, search):
    query = parse_qs(search.strip("?"))
    fig_css_args = FigCSSArgs.parse_obj(query)

    try:
        if pathname.startswith("/dash/charts"):
            if pathname in config.charts:
                return create_chart(
                    chart_name=config.charts[pathname],
                    fig_css_args=fig_css_args,
                )

        if pathname.startswith("/dash/tables"):
            if pathname in config.table_snippets:
                return create_table_snippet(
                    table_name=config.table_snippets[pathname],
                    fig_css_args=fig_css_args,
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
    if len(selected_fields) == len(all_options):
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
