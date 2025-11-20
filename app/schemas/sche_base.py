from pydantic import BaseModel, Field
from typing import Optional, Literal


class BaseModelResponse(BaseModel):
    id: int
    created_at: float
    updated_at: float


class PaginationParams(BaseModel):
    page_size: Optional[int] = Field(default=10, gt=0, le=100)
    page: Optional[int] = Field(default=1, gt=0)


class SortParams(BaseModel):
    sort_by: Optional[str] = "id"
    order: Optional[Literal["asc", "desc"]] = "desc"
