from pathlib import PosixPath
from typing import Union

from pydantic import BaseModel


class GraphMeta(BaseModel):
    path: Union[str, PosixPath]


class SuccessResponse(BaseModel):
    data: GraphMeta
