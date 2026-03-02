from pydantic import BaseModel,Field

class CategoryCreate(BaseModel):
    name: str
    type: str
    description: str | None = None

class CategoryUpdate(BaseModel):
    name: str = Field(...,min_length=1,max_length=100)
    type: str = Field(..., pattern="^(income|expense|both)$")
    description: str | None = Field(None, max_length=500)
