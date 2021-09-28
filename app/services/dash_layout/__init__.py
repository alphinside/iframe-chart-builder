from app.schema.requests import ChartStyle


def create_default_chart_style():
    return ChartStyle(
        figure={"height": "50vh", "width": "100vh", "display": "inline-block"},
        filters_group={
            "height": "50vh",
            "width": "20vh",
            "display": "inline-block",
            "vertical-align": "top",
        },
        filters_entity={},
    )
