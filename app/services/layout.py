from typing import Any, Dict, Optional

import plotly.figure_factory as ff
from dash import dcc, html
from pydantic import BaseModel
from pydantic.class_validators import root_validator

from app.data_manager import get_data


class FigSize(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None

    @root_validator(pre=True)
    def cast_chart_params(cls, values):
        if "width" in values:
            values["width"] = int(values["width"][0])

        if "height" in values:
            values["height"] = int(values["height"][0])

        return values


def create_table_layout(table_name: str, query: Dict[str, Any]):
    df = get_data(table_name)

    figsize = FigSize.parse_obj(query)

    fig = ff.create_table(df.head(5))

    if figsize.width is not None:
        fig.layout.width = figsize.width

    if figsize.width is not None:
        fig.layout.height = figsize.height

    return html.Div([dcc.Graph(figure=fig)])
