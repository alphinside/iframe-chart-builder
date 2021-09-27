import plotly.figure_factory as ff
from dash import dcc

from app.constant import TABLES_ROUTE
from app.data_manager import get_data
from app.schema.requests import ChartStyle
from app.utils import check_validate_style_config


def create_table_snippet(table_name: str):
    df = get_data(table_name)

    fig = ff.create_table(df.head(5), height_constant=20)

    style = check_validate_style_config(name=table_name, route=TABLES_ROUTE)

    return [dcc.Graph(figure=fig, style=style.table)]


def create_default_table_style_config():
    return ChartStyle(table={"width": "50vh", "height": "30vh"})
