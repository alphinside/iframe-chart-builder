from http import HTTPStatus
from urllib.parse import parse_qs

import config
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Response

from app.constant import DASH_ROOT_ROUTE
from app.schema.requests import FigSize
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
    figsize = FigSize.parse_obj(query)

    try:
        if pathname.startswith("/dash/charts"):
            if pathname in config.charts:
                return create_chart(
                    chart_name=config.charts[pathname], figsize=figsize
                )

        if pathname.startswith("/dash/tables"):
            if pathname in config.table_snippets:
                return create_table_snippet(
                    table_name=config.table_snippets[pathname], figsize=figsize
                )

        Response("404 Not Found", HTTPStatus.NOT_FOUND)
        return [html.H1("404 Not Found")]

    except Exception as e:
        Response(
            f"500 Internal Server Error : {e}",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return [html.H1(f"500 Internal Server Error : {e}")]
