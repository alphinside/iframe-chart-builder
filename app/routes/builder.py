from http import HTTPStatus
from typing import Type

import pandas as pd
from fastapi import (
    APIRouter,
    Body,
    File,
    Form,
    HTTPException,
    Path,
    UploadFile,
)

from app.config import get_settings
from app.constant import (
    CHARTS_ROUTE,
    STANDARD_DATA_FILENAME,
    STANDARD_STYLE_CONFIG,
    TABLES_ROUTE,
    ResourceType,
)
from app.data_manager import register_chart_path, register_table_path
from app.schema.requests import (
    BarChartBuilderRequest,
    BaseChartBuilderRequest,
    ChartStyle,
    ChoroplethMapBuilderRequest,
)
from app.schema.response import (
    ChartBuilderData,
    ChartBuilderResponse,
    GeneralSuccessMessage,
    SuccessMessage,
    UploadSuccessData,
    UploadSuccessResponse,
)
from app.services.chart_factory import ChartBuilderService
from app.services.dash_layout.table import create_default_table_style_config
from app.services.validator import (
    validate_file_suffix,
    validate_resource_existence,
)
from app.utils import (
    construct_standard_dash_url,
    serialize_config,
    serialize_data,
)

router = APIRouter()


@router.post(
    "/table/upload",
    response_model=UploadSuccessResponse,
    summary="Upload new data",
    name="upload data",
)
async def upload(
    table_name: str = Form("", example="example_choropleth_map"),
    error_if_exist: bool = Form(True),
    data: UploadFile = File(...),
):
    data_standardized_name = STANDARD_DATA_FILENAME
    output_dir = get_settings().tables_output_dir / table_name

    validate_file_suffix(data.filename)

    table_name = table_name.strip()
    if table_name == "":
        table_name = data.filename.strip(".xlsx")

    if error_if_exist and output_dir.exists():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"table `{table_name}` is already exist",
        )

    uploaded_data = await data.read()
    df = pd.read_excel(uploaded_data)

    serialize_data(
        df=df, filename=data_standardized_name, output_dir=output_dir
    )

    table_snippet_url = construct_standard_dash_url(
        name=table_name, route=TABLES_ROUTE
    )

    table_default_style = create_default_table_style_config()
    serialize_config(
        config=table_default_style,
        output_dir=output_dir,
        filename=STANDARD_STYLE_CONFIG,
    )

    register_table_path(
        table_name=table_name, table_snippet_url=table_snippet_url
    )

    return UploadSuccessResponse(
        data=UploadSuccessData(
            table_name=table_name, table_snippet_url=table_snippet_url
        )
    )


def register_chart_config(request: Type[BaseChartBuilderRequest]):
    service = ChartBuilderService(request.chart_type)
    service.load_and_evaluate_data(
        table_name=request.table_name, chart_params=request.chart_params
    )
    service.dump_config(request)

    chart_url = construct_standard_dash_url(
        name=request.chart_name, route=CHARTS_ROUTE
    )

    register_chart_path(chart_name=request.chart_name, chart_url=chart_url)

    return chart_url


@router.post(
    "/chart/bar",
    response_model=ChartBuilderResponse,
    summary="Create new bar chart iframe",
    name="create_new_bar_chart",
)
async def register_new_bar_chart(request: BarChartBuilderRequest):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/chart/choropleth_map",
    response_model=ChartBuilderResponse,
    summary="Create new choropleth map chart iframe",
    name="create_new_choropleth_map_chart",
)
async def register_new_choropleth_map(request: ChoroplethMapBuilderRequest):
    chart_url = register_chart_config(request)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )


@router.post(
    "/{resource}/{name}/style-config", response_model=GeneralSuccessMessage
)
async def update_style_config(
    resource: ResourceType = Path(..., example="chart"),
    name: str = Path(..., example="provinces_residents"),
    style: ChartStyle = Body(
        ...,
        example=ChartStyle(
            figure={"height": "50vh", "width": "80vh"},
            filters_parent={
                "height": "50vh",
                "width": "20vh",
            },
            table={"width": "50vh", "height": "30vh"},
        ),
    ),
):
    resource_path = validate_resource_existence(name=name, resource=resource)

    serialize_config(
        config=style, output_dir=resource_path, filename=STANDARD_STYLE_CONFIG
    )

    return GeneralSuccessMessage(data=SuccessMessage())


@router.get("/{resource}/{name}/style-config", response_model=ChartStyle)
async def get_style_config(
    resource: ResourceType = Path(..., example="chart"),
    name: str = Path(..., example="provinces_residents"),
):
    resource_path = validate_resource_existence(name=name, resource=resource)

    style_config = resource_path / STANDARD_STYLE_CONFIG

    return ChartStyle.parse_file(style_config)