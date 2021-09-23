from pathlib import PosixPath

from pydantic import BaseModel


class SuccessMessage(BaseModel):
    chart_url: PosixPath


class SuccessResponse(BaseModel):
    data: SuccessMessage
