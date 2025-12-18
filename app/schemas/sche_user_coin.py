from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class UserCoinCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    coin: Optional[int] = Field(0, ge=0, example=100, description="Số coin ban đầu (integer, >= 0, mặc định: 0)")


class UserCoinUpdateRequest(BaseModel):
    coin: Optional[int] = Field(None, ge=0, example=150, description="Số coin mới (integer, >= 0)")


class UserCoinBaseResponse(BaseModel):
    coin_id: int = Field(..., description="ID của coin record (integer)")
    user_id: int = Field(..., description="ID của user sở hữu coin (integer)")
    coin: int = Field(..., description="Số coin hiện tại (integer)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

    class Config:
        from_attributes = True

