from pydantic import BaseModel

from app.constant import ChartTypes


class ChartCreationRequest(BaseModel):
    chart_type: ChartTypes
