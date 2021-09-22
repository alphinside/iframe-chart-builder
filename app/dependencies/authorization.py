from http import HTTPStatus

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.config import get_settings

api_key_header_auth = APIKeyHeader(name="Authorization", auto_error=True)


def get_api_key_authorization(
    api_key_header: str = Security(api_key_header_auth),
):
    if api_key_header != f"Bearer {get_settings().service_api_key}":
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="wrong API key"
        )
