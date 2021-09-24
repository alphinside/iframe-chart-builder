from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, Form, UploadFile

from app.config import get_settings
from app.constant import DASH_MOUNT_ROUTE, STANDARD_DATA_FILENAME, TABLES_ROUTE
from app.schema.response import UploadSuccessData, UploadSuccessResponse
from app.services.validator import validate_file_suffix
from app.utils import serialize_data

router = APIRouter()


@router.post(
    "/upload-data",
    response_model=UploadSuccessResponse,
    summary="Upload new data",
    name="upload data",
)
async def upload(table_name: str = Form(""), data: UploadFile = File(...)):
    validate_file_suffix(data.filename)

    table_name = table_name.strip()
    if table_name == "":
        table_name = data.filename.strip(".xlsx")

    uploaded_data = await data.read()
    df = pd.read_excel(uploaded_data)

    data_standardized_name = STANDARD_DATA_FILENAME
    output_dir = get_settings().tables_output_dir / table_name
    serialize_data(
        df=df, filename=data_standardized_name, output_dir=output_dir
    )

    table_snippet_url = Path(DASH_MOUNT_ROUTE + TABLES_ROUTE) / table_name

    return UploadSuccessResponse(
        data=UploadSuccessData(
            table_name=table_name, table_snippet_url=table_snippet_url
        )
    )


# @router.post(
#     "/new-chart",
#     response_model=SuccessResponse,
#     summary="Create new chart iframe",
#     name="create_new_chart",
# )
# async def create(
#     request: Json[ChartBuilderRequest] = Form(...),
#     ,
# ):


#     service = ChartBuilderService(request)
#     service.eval_and_dump_config(
#         filename=data.filename, uploaded_data=uploaded_data
#     )

#     chart_url = "asd"
#     return SuccessResponse(data=SuccessMessage(chart_url=chart_url))
