from typing import List

import pandas as pd
from dash import dcc, html

from app.constant import (
    COLUMN_FILTER_CAT,
    COLUMN_FILTER_SELECT_ALL,
    SELECT_ALL_VALUE,
    DataTypes,
)
from app.schema.params import ColumnFilter


def create_filters_control(df: pd.DataFrame, filters: List[ColumnFilter]):
    created_filters = []

    for filter in filters:
        if filter.type == DataTypes.categorical:
            cat_filter = create_categorical_filter(df=df, filter=filter)
            created_filters.append(cat_filter)
        elif filter.type == DataTypes.numerical:
            created_filters.append(html.Div())
        else:
            raise Exception("Unknown filter creation error")

    return html.Div(created_filters)


def create_categorical_filter(df: pd.DataFrame, filter: ColumnFilter):
    categorical_selection = [
        {"label": k, "value": k} for k in sorted(df[filter.column].unique())
    ]

    dropdown = html.Div(
        [
            dcc.Markdown(f"**{filter.column.title()}**"),
            html.Div(
                [
                    dcc.Dropdown(
                        id={"index": filter.column, "type": COLUMN_FILTER_CAT},
                        multi=True,
                        options=categorical_selection,
                        searchable=True,
                    )
                ]
            ),
            html.Div(
                [
                    dcc.Checklist(
                        id={
                            "index": filter.column,
                            "type": COLUMN_FILTER_SELECT_ALL,
                        },
                        options=[
                            {"label": "Select All", "value": SELECT_ALL_VALUE}
                        ],
                    )
                ]
            ),
        ],
    )

    return dropdown
