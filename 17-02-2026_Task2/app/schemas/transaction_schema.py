from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime,timezone

class TransactionCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    amount: float
    type: str
    category: str
    date: datetime
    tags: List[str] = []

    @field_validator("title")
    def strip_title(cls, v): return v.strip()

    @field_validator("amount")
    def validate_amount(cls, v):
        if v <= 0: raise ValueError("Amount must be > 0")
        return v

    @field_validator("type")
    def validate_type(cls, v):
        if v not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return v

    @field_validator("category")
    def validate_category(cls, v):
        if not v: raise ValueError("Category required")
        return v.lower()

    @field_validator("date")
    def not_future(cls, v):
        from datetime import datetime
        if v > datetime.now(timezone.utc):
            raise ValueError("Future date not allowed")
        return v

    @field_validator("tags")
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError("Max 10 tags allowed")
        for tag in v:
            if len(tag) > 30:
                raise ValueError("Tag too long")
        return v

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    tags: Optional[List[str]] = None