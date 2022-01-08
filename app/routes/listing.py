import os
import shutil
from datetime import datetime
from http import HTTPStatus
from typing import List

import config
import pandas as pd
import plotly.express as px
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
    STANDARD_CHARTS_CONFIG,
    STANDARD_DATA_FILENAME,
    STANDARD_STYLE_CONFIG,
    ChartTypes,
    ExtendedResourceType,
    PlotlyColorGroup,
    ResourceType,
)
from app.data_manager import register_table_path
from app.schema.requests import ChartStyle
from app.schema.response import (
    ColorGroupResponse,
    ColorGroupsModel,
    ColorOptionsResponse,
    GeneralSuccessResponse,
    Listing,
    ListingResponse,
    PaginationMeta,
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
    check_validate_chart_config,
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

    table_name = table_name.strip()
    if table_name == "":
        table_name = data.filename.strip(".xlsx")

    output_dir = get_settings().tables_output_dir / table_name

    validate_file_suffix(data.filename)

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
        name=table_name, resource_type=ResourceType.table
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


@router.get(
    "/tables", response_model=ListingResponse, summary="Get table listing"
)
async def get_tables(current_page: int = 1, page_size: int = 10):
    tables = []

    start_idx_range = (current_page - 1) * page_size
    end_idx_range = current_page * page_size

    paged_items = list(config.table_snippets.items())[
        start_idx_range:end_idx_range
    ]

    for url, name in paged_items:
        data_path = (
            get_settings().tables_output_dir / name / STANDARD_DATA_FILENAME
        )
        created_at = datetime.fromtimestamp(
            os.path.getctime(data_path)
        ).isoformat()
        modified_at = datetime.fromtimestamp(
            os.path.getmtime(data_path)
        ).isoformat()
        tables.append(
            Listing(
                name=name,
                url=url,
                type=ChartTypes.table,
                created_at=created_at,
                modified_at=modified_at,
            )
        )

    return ListingResponse(
        data=tables,
        meta=PaginationMeta(
            current_page=current_page,
            page_size=page_size,
            total=len(config.table_snippets.items()),
        ),
    )


@router.get(
    "/charts", response_model=ListingResponse, summary="Get chart listing"
)
async def get_charts(current_page: int = 1, page_size: int = 10):
    charts = []

    start_idx_range = (current_page - 1) * page_size
    end_idx_range = current_page * page_size

    paged_items = list(config.charts.items())[start_idx_range:end_idx_range]

    for url, name in paged_items:
        chart_config = check_validate_chart_config(name)
        created_at = datetime.fromtimestamp(
            os.path.getctime(
                get_settings().charts_output_dir
                / name
                / STANDARD_CHARTS_CONFIG
            )
        ).isoformat()
        modified_at = datetime.fromtimestamp(
            os.path.getmtime(
                get_settings().charts_output_dir / name / STANDARD_STYLE_CONFIG
            )
        ).isoformat()
        charts.append(
            Listing(
                name=name,
                url=url,
                type=chart_config.chart_type,
                created_at=created_at,
                modified_at=modified_at,
            )
        )

    return ListingResponse(
        data=charts,
        meta=PaginationMeta(
            current_page=current_page,
            page_size=page_size,
            total=len(config.charts.items()),
        ),
    )


@router.get(
    "/color-options",
    response_model=ColorOptionsResponse,
    summary="Get all built-in color options",
)
async def get_built_in_color():
    def _list_available_color_names(group: PlotlyColorGroup) -> List[str]:
        color_group_object = getattr(px.colors, group)
        available_colors = [
            set(data.y).pop() for data in color_group_object.swatches().data
        ]

        return available_colors

    built_in_colors = {
        k.name: ColorGroupResponse(
            snippet_url=construct_standard_dash_url(
                name=k.name, resource_type=ExtendedResourceType.color_group
            ),
            colors_list=_list_available_color_names(k),
        )
        for k in PlotlyColorGroup
    }

    return ColorOptionsResponse(data=ColorGroupsModel(**built_in_colors))


@router.delete(
    "/{resource}/{name}",
    response_model=GeneralSuccessResponse,
    summary="Delete resources",
)
async def delete_resources(
    resource: ResourceType = Path(..., example="chart"),
    name: str = Path(..., example="example_choropleth_map"),
):

    resource_path = validate_resource_existence(name=name, resource=resource)

    if resource == ResourceType.chart:
        url = construct_standard_dash_url(
            name=name, resource_type=ResourceType.chart
        )
        config.charts.pop(url, None)
    elif resource == ResourceType.table:
        url = construct_standard_dash_url(
            name=name, resource_type=ResourceType.table
        )
        config.table_snippets.pop(url, None)
        config.table_dfs.pop(name, None)
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"resource `{resource} {name}` not found",
        )

    shutil.rmtree(resource_path)

    return GeneralSuccessResponse(data=SuccessMessage())


@router.post(
    "/{resource}/{name}/style-config",
    response_model=GeneralSuccessResponse,
    summary="Update chart HTML div styling",
)
async def update_style_config(
    resource: ResourceType = Path(..., example="chart"),
    name: str = Path(..., example="example_choropleth_map"),
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


@router.get(
    "/{resource}/{name}/style-config",
    response_model=ChartStyle,
    summary="Get current chart HTML div styling",
)
async def get_style_config(
    resource: ResourceType = Path(..., example="chart"),
    name: str = Path(..., example="example_choropleth_map"),
):
    resource_path = validate_resource_existence(name=name, resource=resource)

    style_config = resource_path / STANDARD_STYLE_CONFIG

    return ChartStyle.parse_file(style_config)
