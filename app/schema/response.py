from pathlib import PosixPath

from pydantic import BaseModel


class UploadSuccessData(BaseModel):
    table_name: str
    table_snippet_url: PosixPath


class UploadSuccessResponse(BaseModel):
    data: UploadSuccessData
