from http import HTTPStatus

import config
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Response

from app.constant import DASH_ROOT_ROUTE

dash_app = dash.Dash(__name__, requests_pathname_prefix=DASH_ROOT_ROUTE)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame(
    {
        "Fruit": [
            "Apples",
            "Oranges",
            "Bananas",
            "Apples",
            "Oranges",
            "Bananas",
        ],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(
    df,
    x="Fruit",
    y="Amount",
    color="City",
    barmode="group",
    width=800,
    height=600,
)

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@dash_app.callback(
    Output("page-content", "children"), [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname.startswith("/dash/charts"):
        return html.Div(html.H1("HELLO WORLD"))
    if pathname.startswith("/dash/tables"):
        import pdb

        pdb.set_trace()
        if pathname in config.table_snippets:
            return html.Div(html.H1("HELLO WORLD"))

    Response("404 Not Found", HTTPStatus.NOT_FOUND)
    return html.Div("404 Not Found")
