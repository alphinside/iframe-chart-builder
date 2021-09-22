from pydantic import BaseModel


class SuccessMessage(BaseModel):
    message: str = "success"


class SuccessResponse(BaseModel):
    data: SuccessMessage = SuccessMessage()
