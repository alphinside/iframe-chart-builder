from fastapi import APIRouter, Depends

from app.dependencies.authorization import get_api_key_authorization
from app.routes import charts_builder

api_router = APIRouter()

api_router.include_router(
    charts_builder.router,
    tags=["charts_builder"],
    prefix="/charts_builder",
    dependencies=[Depends(get_api_key_authorization)],
)
