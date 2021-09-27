import plotly.figure_factory as ff
from dash import dcc

from app.data_manager import get_data
from app.schema.requests import TableStyle


def create_table_snippet(table_name: str):
    df = get_data(table_name)

    fig = ff.create_table(df.head(5), height_constant=20)

    return [dcc.Graph(figure=fig)]


def create_default_table_style_config():
    return TableStyle(table={"width": "50vh", "height": "30vh"})
