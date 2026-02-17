from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    type: str
    description: str | None = None
class CategoryUpdate(BaseModel):
    description: str | None = None
