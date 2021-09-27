from http import HTTPStatus
from pathlib import Path, PosixPath

from fastapi import HTTPException

from app.config import get_settings
from app.constant import (
    STANDARD_CHARTS_CONFIG,
    STANDARD_DATA_FILENAME,
    STANDARD_STYLE_CONFIG,
    ResourceType,
)


def validate_file_suffix(filename: str):
    if not Path(filename).suffix == ".xlsx":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="uploaded file is not .xlsx file",
        )


def validate_resource_existence(
    name: str, resource: ResourceType
) -> PosixPath:
    if resource == ResourceType.table:
        resource_path = get_settings().tables_output_dir / name
    elif resource == ResourceType.chart:
        resource_path = get_settings().charts_output_dir / name
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"unknown resource `{resource}`",
        )

    if not resource_path.exists():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"resource `{resource} {name}` not found",
        )

    if resource == ResourceType.table:
        data = resource_path / STANDARD_DATA_FILENAME
        if not data.exists():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"resource `{resource} {name}` "
                f"{STANDARD_DATA_FILENAME} not found",
            )

    elif resource == ResourceType.chart:
        charts_config = resource_path / STANDARD_CHARTS_CONFIG
        if not charts_config.exists():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"resource `{resource} {name}` "
                f"{STANDARD_CHARTS_CONFIG} not found",
            )
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"unknown resource `{resource}`",
        )

    style_config = resource_path / STANDARD_STYLE_CONFIG
    if not style_config.exists():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"resource `{resource} {name}` "
            f"{STANDARD_STYLE_CONFIG} not found",
        )

    return resource_path
