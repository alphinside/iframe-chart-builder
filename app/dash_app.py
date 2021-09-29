import logging
from http import HTTPStatus

import config
import dash
from dash import dcc, html
from dash.dependencies import ALL, MATCH, Input, Output, State
from flask import Response

from app.constant import (
    CHARTS_ROUTE,
    COLUMN_FILTER_CAT,
    COLUMN_FILTER_NUM_MAX,
    COLUMN_FILTER_NUM_MIN,
    COLUMN_FILTER_SELECT_ALL,
    DASH_MOUNT_ROUTE,
    DASH_ROOT_ROUTE,
    SELECT_ALL_VALUE,
    TABLES_ROUTE,
)
from app.data_manager import get_charts_meta
from app.schema.params import (
    AppliedFilters,
    CategoricalFilterState,
    MinMaxNumericalFilterState,
)
from app.services.chart_factory import create_chart
from app.services.dash_layout.chart import create_chart_content
from app.services.dash_layout.table import create_table_snippet

dash_app = dash.Dash(__name__, requests_pathname_prefix=DASH_ROOT_ROUTE)

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@dash_app.callback(
    output=Output({"type": COLUMN_FILTER_SELECT_ALL, "index": MATCH}, "value"),
    inputs={
        "selected_fields": Input(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "value"
        ),
        "all_options": State(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "options"
        ),
    },
)
def select_all_cat_activation(selected_fields, all_options):
    if selected_fields is not None and len(selected_fields) == len(
        all_options
    ):
        return [SELECT_ALL_VALUE]

    return []


@dash_app.callback(
    output=Output({"type": COLUMN_FILTER_CAT, "index": MATCH}, "value"),
    inputs={
        "selected_fields": Input(
            {"type": COLUMN_FILTER_SELECT_ALL, "index": MATCH}, "value"
        ),
        "all_options": State(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "options"
        ),
        "active_state": State(
            {"type": COLUMN_FILTER_CAT, "index": MATCH}, "value"
        ),
    },
)
def link_select_all_to_multi_select(
    selected_fields, all_options, active_state
):
    if selected_fields == [SELECT_ALL_VALUE]:
        return [option["value"] for option in all_options]

    return active_state


@dash_app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_initial_page(pathname):
    try:
        if pathname.startswith(DASH_MOUNT_ROUTE + CHARTS_ROUTE):
            if pathname in config.charts:
                df, config_model = get_charts_meta(config.charts[pathname])
                fig = create_chart(df=df, config_model=config_model)
                return create_chart_content(
                    chart_name=config.charts[pathname],
                    df=df,
                    fig=fig,
                    filters=config_model.chart_params.filters,
                )

        if pathname.startswith(DASH_MOUNT_ROUTE + TABLES_ROUTE):
            if pathname in config.table_snippets:
                return create_table_snippet(
                    table_name=config.table_snippets[pathname]
                )

        Response("404 Not Found", HTTPStatus.NOT_FOUND)
        return [html.H1("404 Not Found")]

    except Exception as e:
        Response(
            f"500 Internal Server Error : {e}",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return [html.H1(f"500 Internal Server Error : {e}")]


@dash_app.callback(
    output=Output("chart", "figure"),
    inputs={
        "cat_values": Input(
            {"type": COLUMN_FILTER_CAT, "index": ALL}, "value"
        ),
        "num_values_min": Input(
            {"type": COLUMN_FILTER_NUM_MIN, "index": ALL}, "value"
        ),
        "num_values_max": Input(
            {"type": COLUMN_FILTER_NUM_MAX, "index": ALL}, "value"
        ),
        "cat_options": State(
            {"type": COLUMN_FILTER_CAT, "index": ALL}, "options"
        ),
        "num_column_min": State(
            {"type": COLUMN_FILTER_NUM_MIN, "index": ALL}, "min"
        ),
        "num_column_max": State(
            {"type": COLUMN_FILTER_NUM_MAX, "index": ALL}, "max"
        ),
        "cat_id": State({"type": COLUMN_FILTER_CAT, "index": ALL}, "id"),
        "num_id": State({"type": COLUMN_FILTER_NUM_MIN, "index": ALL}, "id"),
        "pathname": State("url", "pathname"),
        "current_fig": State("chart", "figure"),
    },
)
def update_chart_based_on_filter(
    cat_values,
    num_values_min,
    num_values_max,
    cat_options,
    num_column_min,
    num_column_max,
    cat_id,
    num_id,
    pathname,
    current_fig,
):
    ctx = dash.callback_context

    if not ctx.triggered:
        return current_fig

    applied_filters = _build_filters(
        cat_values,
        num_values_min,
        num_values_max,
        cat_options,
        num_column_min,
        num_column_max,
        cat_id,
        num_id,
    )

    try:
        df, config_model = get_charts_meta(config.charts[pathname])
        updated_fig = create_chart(
            df=df,
            config_model=config_model,
            applied_filters=applied_filters,
        )

        return updated_fig
    except Exception as e:
        logging.error(e)
        return current_fig


# TODO handle numerical
def _build_filters(
    cat_values,
    num_values_min,
    num_values_max,
    cat_options,
    num_column_min,
    num_column_max,
    cat_id,
    num_id,
) -> AppliedFilters:
    cat_filters = []
    num_filters = []

    for values, options, column in zip(cat_values, cat_options, cat_id):
        if values is None or len(values) == 0 or len(values) == len(options):
            continue

        column_filter = CategoricalFilterState(
            column=column["index"], values=values
        )
        cat_filters.append(column_filter)

    for values_min, values_max, column_min, column_max, column in zip(
        num_values_min, num_values_max, num_column_min, num_column_max, num_id
    ):
        if (values_min is None or values_min < column_min) and (
            values_max is None or values_max > column_max
        ):
            continue

        column_filter = MinMaxNumericalFilterState(
            column=column["index"],
            column_min=column_min,
            column_max=column_max,
            values_min=values_min,
            values_max=values_max,
        )
        num_filters.append(column_filter)

    return AppliedFilters(categorical=cat_filters, numerical=num_filters)
