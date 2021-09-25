from http import HTTPStatus

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.constant import CHARTS_ROUTE, STANDARD_DATA_FILENAME, TABLES_ROUTE
from app.data_manager import register_chart_path, register_table_path
from app.schema.requests import ChartBuilderRequest
from app.schema.response import (
    ChartBuilderData,
    ChartBuilderResponse,
    UploadSuccessData,
    UploadSuccessResponse,
)
from app.services.chart_factory import ChartBuilderService
from app.services.validator import validate_file_suffix
from app.utils import construct_standard_dash_url, serialize_data

router = APIRouter()


@router.post(
    "/upload-data",
    response_model=UploadSuccessResponse,
    summary="Upload new data",
    name="upload data",
)
async def upload(
    table_name: str = Form(""),
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

    register_table_path(
        table_name=table_name, table_snippet_url=table_snippet_url
    )

    return UploadSuccessResponse(
        data=UploadSuccessData(
            table_name=table_name, table_snippet_url=table_snippet_url
        )
    )


@router.post(
    "/new-chart",
    response_model=ChartBuilderResponse,
    summary="Create new chart iframe",
    name="create_new_chart",
)
async def create(request: ChartBuilderRequest):
    service = ChartBuilderService(request.chart_type)
    service.load_and_evaluate_data(
        table_name=request.table_name, chart_params=request.chart_params
    )
    service.dump_config(request)

    chart_url = construct_standard_dash_url(
        name=request.chart_name, route=CHARTS_ROUTE
    )

    register_chart_path(chart_name=request.chart_name, chart_url=chart_url)

    return ChartBuilderResponse(
        data=ChartBuilderData(
            chart_name=request.chart_name, chart_url=chart_url
        )
    )
