from typing import List

import pandas as pd
from dash import dcc, html

from app.constant import (
    COLUMN_FILTER_CAT,
    COLUMN_FILTER_NUM_MAX,
    COLUMN_FILTER_NUM_MIN,
    COLUMN_FILTER_SELECT_ALL,
    SELECT_ALL_VALUE,
    DataTypes,
)
from app.schema.params import ColumnFilter
from app.schema.requests import StyleDict


def create_filters_control(
    df: pd.DataFrame, filters: List[ColumnFilter], style: StyleDict
):
    created_filters = []

    for filter in filters:
        if filter.type == DataTypes.categorical:
            cat_filter = create_categorical_filter(df=df, filter=filter)
            created_filters.append(cat_filter)
        elif filter.type == DataTypes.numerical:
            num_filter = create_numerical_filter(df=df, filter=filter)
            created_filters.append(num_filter)
        else:
            raise Exception("Unknown filter creation error")

    return html.Div(created_filters, style=style)


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


def create_numerical_filter(df: pd.DataFrame, filter: ColumnFilter):
    min_val, max_val = df[filter.column].min(), df[filter.column].max()
    formatted_min = "{:0,.2f}".format(min_val)
    formatted_max = "{:0,.2f}".format(max_val)

    input_fields = html.Div(
        [
            dcc.Markdown(f"**{filter.column.title()}**"),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Markdown(f"*minimum : {formatted_min}*"),
                            dcc.Input(
                                id={
                                    "index": filter.column,
                                    "type": COLUMN_FILTER_NUM_MIN,
                                },
                                placeholder="Enter filter min value...",
                                type="number",
                                min=min_val,
                                max=max_val,
                                value=None,
                                style={
                                    "margin-right": "1vh",
                                    "margin-bottom": "1vh",
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            dcc.Markdown(f"*maximum : {formatted_max}*"),
                            dcc.Input(
                                id={
                                    "index": filter.column,
                                    "type": COLUMN_FILTER_NUM_MAX,
                                },
                                placeholder="Enter filter max value...",
                                type="number",
                                min=min_val,
                                max=max_val,
                                value=None,
                                style={
                                    "margin-right": "1vh",
                                    "margin-bottom": "1vh",
                                },
                            ),
                        ],
                    ),
                ],
                style={"display": "flex"},
            ),
        ]
    )

    return input_fields
