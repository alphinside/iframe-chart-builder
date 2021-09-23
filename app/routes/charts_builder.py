from fastapi import APIRouter, File, Form, UploadFile
from pydantic import Json

from app.schema import SuccessMessage, SuccessResponse
from app.schema.requests import ChartBuilderRequest
from app.services.factory import ChartBuilderService
from app.services.validator import validate_file_suffix

router = APIRouter()


@router.post(
    "/new-chart",
    response_model=SuccessResponse,
    summary="Create new chart iframe",
    name="create_new_chart",
)
async def create(
    request: Json[ChartBuilderRequest] = Form(...),
    data: UploadFile = File(...),
):
    validate_file_suffix(data.filename)

    uploaded_data = await data.read()

    service = ChartBuilderService(request)
    chart_url = service.build(
        filename=data.filename, uploaded_data=uploaded_data
    )

    return SuccessResponse(data=SuccessMessage(chart_url=chart_url))
