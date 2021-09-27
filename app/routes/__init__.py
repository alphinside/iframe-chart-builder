from fastapi import APIRouter, Depends

from app.dependencies.authorization import get_api_key_authorization
from app.routes import builder

api_router = APIRouter()

api_router.include_router(
    builder.router,
    tags=["builder"],
    prefix="/builder",
    dependencies=[Depends(get_api_key_authorization)],
)
