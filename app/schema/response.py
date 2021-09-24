from pathlib import PosixPath
from typing import Union

from pydantic import BaseModel


class UploadSuccessData(BaseModel):
    table_name: str
    table_snippet_url: Union[str, PosixPath]


class ChartBuilderData(BaseModel):
    chart_name: str
    chart_url: Union[str, PosixPath]


class UploadSuccessResponse(BaseModel):
    data: UploadSuccessData


class ChartBuilderResponse(BaseModel):
    data: ChartBuilderData
