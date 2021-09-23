from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException


def validate_file_suffix(filename: str):
    if not Path(filename).suffix == ".xlsx":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="uploaded file is not .xlsx file",
        )
