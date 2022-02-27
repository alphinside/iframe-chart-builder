from typing import Type

from fastapi import APIRouter, Body

from app.constant import ResourceType
from app.data_manager import register_chart_path
from app.schema.examples import (
    BARCHART_REQUEST_EXAMPLES,
    BUBBLECHART_REQUEST_EXAMPLES,
    BUBBLEMAP_REQUEST_EXAMPLES,
    CHOROPLETHMAP_REQUEST_EXAMPLES,
    LINECHART_REQUEST_EXAMPLES,
    PIECHART_REQUEST_EXAMPLES,
    RADARCHART_REQUEST_EXAMPLES,
    SUNBURSTCHART_REQUEST_EXAMPLES,
    WINDROSECHART_REQUEST_EXAMPLES,
)
from app.schema.requests import (
    BarChartBuilderRequest,
    BaseChartBuilderRequest,
    BubbleChartBuilderRequest,
    BubbleMapBuilderRequest,
    ChoroplethMapBuilderRequest,
    LineChartBuilderRequest,
    PieChartBuilderRequest,
    RadarChartBuilderRequest,
    SunburstChartBuilderRequest,
    WindroseChartBuilderRequest,
)
from app.schema.response import ChartBuilderData, ChartBuilderResponse
from app.services.chart_factory import ChartBuilderService
from app.utils import construct_standard_dash_url

router = APIRouter()


def register_chart_config(request: Type[BaseChartBuilderRequest]):
    service = ChartBuilderService(request.chart_type)
    service.load_and_evaluate_data(
        table_name=request.table_name, chart_params=request.chart_params
    )
    service.dump_config(request)

    chart_url = construct_standard_dash_url(
        name=request.chart_name, resource_type=ResourceType.chart
    )

    register_chart_path(chart_name=request.chart_name, chart_url=chart_url)

    return chart_url


@router.post(
    "/chart/bar",
    response_model=ChartBuilderResponse,
    summary="Create new bar chart",
    name="create_new_bar_chart",
)
def register_new_bar_chart(
    request: BarChartBuilderRequest = Body(
        ..., examples=BARCHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/choropleth-map",
    response_model=ChartBuilderResponse,
    summary="Create new choropleth map chart",
    name="create_new_choropleth_map_chart",
)
def register_new_choropleth_map(
    request: ChoroplethMapBuilderRequest = Body(
        ..., examples=CHOROPLETHMAP_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/bubble-map",
    response_model=ChartBuilderResponse,
    summary="Create new bubble / scatter map chart",
    name="create_new_bubble_map_chart",
)
def register_new_bubble_map(
    request: BubbleMapBuilderRequest = Body(
        ..., examples=BUBBLEMAP_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/bubble",
    response_model=ChartBuilderResponse,
    summary="Create new bubble / scatter chart",
    name="create_new_bubble_chart",
)
def register_new_bubble_chart(
    request: BubbleChartBuilderRequest = Body(
        ..., examples=BUBBLECHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/line",
    response_model=ChartBuilderResponse,
    summary="Create new line chart",
    name="create_new_line_chart",
)
def register_new_line_chart(
    request: LineChartBuilderRequest = Body(
        ..., examples=LINECHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/pie",
    response_model=ChartBuilderResponse,
    summary="Create new pie chart",
    name="create_new_pie_chart",
)
def register_new_pie_chart(
    request: PieChartBuilderRequest = Body(
        ..., examples=PIECHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/windrose",
    response_model=ChartBuilderResponse,
    summary="Create new windrose chart",
    name="create_new_windrose_chart",
)
def register_new_windrose_chart(
    request: WindroseChartBuilderRequest = Body(
        ..., examples=WINDROSECHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/sunburst",
    response_model=ChartBuilderResponse,
    summary="Create new sunburst chart",
    name="create_new_sunburst_chart",
)
def register_new_sunburst_chart(
    request: SunburstChartBuilderRequest = Body(
        ..., examples=SUNBURSTCHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/radar",
    response_model=ChartBuilderResponse,
    summary="Create new radar chart",
    name="create_new_radar_chart",
)
def register_new_radar_chart(
    request: RadarChartBuilderRequest = Body(
        ..., examples=RADARCHART_REQUEST_EXAMPLES
    )
):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )
