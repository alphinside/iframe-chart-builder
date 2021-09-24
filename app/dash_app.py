import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html

from app.constant import DASH_ROOT_ROUTE

dash_app = dash.Dash(__name__, requests_pathname_prefix=DASH_ROOT_ROUTE)

table_snippet_resources_list = {}

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
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ]
)
