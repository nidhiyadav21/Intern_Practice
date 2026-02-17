from pydantic import BaseModel,ConfigDict,Field
from typing import Optional,Any

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class SummarySchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)