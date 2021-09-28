from pathlib import PosixPath
from typing import List, Union

from pydantic import BaseModel, Field


class UploadSuccessData(BaseModel):
    table_name: str
    table_snippet_url: Union[str, PosixPath]


class UploadSuccessResponse(BaseModel):
    data: UploadSuccessData


class ChartBuilderData(BaseModel):
    chart_name: str
    chart_url: Union[str, PosixPath]


class ChartBuilderResponse(BaseModel):
    data: ChartBuilderData


class SuccessMessage(BaseModel):
    message: str = Field("success", const=True)


class GeneralSuccessResponse(BaseModel):
    data: SuccessMessage


class Listing(BaseModel):
    name: str
    url: str


class ListingResponse(BaseModel):
    data: List[Listing]
