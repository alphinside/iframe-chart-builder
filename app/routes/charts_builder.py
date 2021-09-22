import uuid

import plotly.express as px
from fastapi import APIRouter

from app.config import get_settings
from app.schema import GraphMeta, SuccessResponse
from app.schema.requests import ChartCreationRequest

router = APIRouter()


@router.post(
    "/new-chart",
    response_model=SuccessResponse,
    summary="Create new chart iframe",
    name="create_new_chart",
)
async def create_new_chart(request: ChartCreationRequest):
    graph_path = get_settings().graphs_output_dir / str(uuid.uuid4())

    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x="year", y="pop")
    fig.write_html(graph_path)

    return SuccessResponse(data=GraphMeta(path=graph_path))
