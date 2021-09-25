import plotly.figure_factory as ff
from dash import dcc

from app.data_manager import get_data
from app.schema.requests import FigSize


def create_table_snippet(table_name: str, figsize: FigSize):
    df = get_data(table_name)

    fig = ff.create_table(df.head(5), height_constant=20)

    fig.layout.width = figsize.width
    fig.layout.height = figsize.height

    return [dcc.Graph(figure=fig)]
