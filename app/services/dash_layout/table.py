import plotly.figure_factory as ff
from dash import dcc

from app.data_manager import get_data
from app.schema.requests import FigCSSArgs


def create_table_snippet(table_name: str, fig_css_args: FigCSSArgs):
    df = get_data(table_name)

    fig = ff.create_table(df.head(5), height_constant=20)

    return [dcc.Graph(figure=fig, style=fig_css_args.dict(exclude_none=True))]
