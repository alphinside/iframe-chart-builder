from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/create-new-chart",
    # response_model=RecommendationResponse,
    # response_model_exclude_none=True,
    # summary="Get user recommendations",
    # description="Get user recommendations from specified id ( user ID /"
    # "session ID ) which calculated from user latest events",
    # name="get_recommendations",
)
async def create_new_chart(chart_type: str):
    return
