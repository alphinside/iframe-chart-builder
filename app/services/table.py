import plotly.figure_factory as ff

from app.data_manager import get_data


def create_table_snippet(table_name: str):
    df = get_data(table_name)

    fig = ff.create_table(df.head(5))

    return fig
