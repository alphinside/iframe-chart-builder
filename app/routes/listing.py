from http import HTTPStatus

import config
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
    STANDARD_DATA_FILENAME,
    STANDARD_STYLE_CONFIG,
    TABLES_ROUTE,
    ResourceType,
)
from app.data_manager import register_table_path
from app.schema.requests import ChartStyle
from app.schema.response import (
    GeneralSuccessResponse,
    Listing,
    ListingResponse,
    SuccessMessage,
    UploadSuccessData,
    UploadSuccessResponse,
)
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


@router.get("/tables", response_model=ListingResponse)
async def get_tables():
    tables = []

    for url, name in config.table_snippets.items():
        tables.append(Listing(name=name, url=url))

    return ListingResponse(data=tables)


@router.get("/charts", response_model=ListingResponse)
async def get_charts():
    charts = []

    for url, name in config.charts.items():
        charts.append(Listing(name=name, url=url))

    return ListingResponse(data=charts)


@router.post(
    "/{resource}/{name}/style-config", response_model=GeneralSuccessResponse
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

    return GeneralSuccessResponse(data=SuccessMessage())


@router.get("/{resource}/{name}/style-config", response_model=ChartStyle)
async def get_style_config(
    resource: ResourceType = Path(..., example="chart"),
    name: str = Path(..., example="provinces_residents"),
):
    resource_path = validate_resource_existence(name=name, resource=resource)

    style_config = resource_path / STANDARD_STYLE_CONFIG

    return ChartStyle.parse_file(style_config)
