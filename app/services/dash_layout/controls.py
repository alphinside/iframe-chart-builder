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
    df: pd.DataFrame,
    filters: List[ColumnFilter],
    group_style: StyleDict = {},
    entity_style: StyleDict = {},
):
    created_filters = []

    for column_filter in filters:
        if column_filter.type == DataTypes.categorical:
            cat_filter = create_categorical_filter(
                df=df, column_filter=column_filter, entity_style=entity_style
            )
            created_filters.append(cat_filter)
        elif column_filter.type == DataTypes.numerical:
            num_filter = create_numerical_filter(
                df=df, column_filter=column_filter, entity_style=entity_style
            )
            created_filters.append(num_filter)
        else:
            raise Exception("Unknown filter creation error")

    if group_style is None:
        group_style = {}

    return html.Div(created_filters, style=group_style)


def create_categorical_filter(
    df: pd.DataFrame, column_filter: ColumnFilter, entity_style: StyleDict
):
    categorical_selection = [
        {"label": k, "value": k}
        for k in sorted(df[column_filter.column].unique())
    ]

    if entity_style is None:
        entity_style = {}

    dropdown = html.Div(
        [
            dcc.Markdown(f"**{column_filter.column.title()}**"),
            dcc.Dropdown(
                id={
                    "index": column_filter.column,
                    "type": COLUMN_FILTER_CAT,
                },
                multi=True,
                options=categorical_selection,
                searchable=True,
            ),
            dcc.Checklist(
                id={
                    "index": column_filter.column,
                    "type": COLUMN_FILTER_SELECT_ALL,
                },
                options=[{"label": "Select All", "value": SELECT_ALL_VALUE}],
            ),
        ],
        style=entity_style,
    )

    return dropdown


def create_numerical_filter(
    df: pd.DataFrame, column_filter: ColumnFilter, entity_style: StyleDict
):
    min_val, max_val = (
        df[column_filter.column].min(),
        df[column_filter.column].max(),
    )
    formatted_min = "{:0,.2f}".format(min_val)
    formatted_max = "{:0,.2f}".format(max_val)

    if entity_style is None:
        entity_style = {}

    input_fields = html.Div(
        [
            dcc.Markdown(f"**{column_filter.column.title()}**"),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Markdown(f"*minimum : {formatted_min}*"),
                            dcc.Input(
                                id={
                                    "index": column_filter.column,
                                    "type": COLUMN_FILTER_NUM_MIN,
                                },
                                placeholder="Enter filter min value...",
                                type="number",
                                min=min_val,
                                max=max_val,
                                value=None,
                                debounce=True,
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
                                    "index": column_filter.column,
                                    "type": COLUMN_FILTER_NUM_MAX,
                                },
                                placeholder="Enter filter max value...",
                                type="number",
                                min=min_val,
                                max=max_val,
                                value=None,
                                debounce=True,
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
        ],
        style=entity_style,
    )

    return input_fields
