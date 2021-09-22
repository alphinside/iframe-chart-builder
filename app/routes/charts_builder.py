from fastapi import APIRouter

from app.schema import SuccessResponse
from app.schema.requests import ChartBuilderRequest
from app.services.factory import ChartBuilderService

router = APIRouter()


@router.post(
    "/new-chart",
    response_model=SuccessResponse,
    summary="Create new chart iframe",
    name="create_new_chart",
)
async def create_new_chart(request: ChartBuilderRequest):
    service = ChartBuilderService(request)
    service.build()

    return SuccessResponse()
