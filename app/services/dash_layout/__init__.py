from app.schema.requests import ChartStyle


def create_default_chart_style():
    return ChartStyle(
        figure={"height": "50vh", "width": "80vh"},
        filters_parent={
            "height": "50vh",
            "width": "20vh",
        },
    )
