from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class GoalCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    goal_date: float = Field(..., example=1703123456.789, description="Ngày của goal (Unix timestamp - float, ví dụ: 1703123456.789)")
    target_sessions: int = Field(..., example=10, description="Số session mục tiêu cần đạt (integer)")
    completed_sessions: Optional[int] = Field(0, example=5, description="Số session đã hoàn thành (integer, mặc định: 0)")
    completion_percentage: Optional[int] = Field(0, example=50, description="Phần trăm hoàn thành (0-100, integer, mặc định: 0)")
    is_achieved: Optional[int] = Field(0, example=0, description="Đã đạt được goal hay chưa: 0 = chưa, 1 = đã đạt (integer, mặc định: 0)")
    achieved_at: Optional[float] = Field(None, example=1703127056.789, description="Thời gian đạt được goal (Unix timestamp - float). Null nếu chưa đạt")


class GoalUpdateRequest(BaseModel):
    goal_date: Optional[float] = Field(None, example=1703123456.789, description="Ngày của goal (Unix timestamp - float)")
    target_sessions: Optional[int] = Field(None, example=10, description="Số session mục tiêu cần đạt (integer)")
    completed_sessions: Optional[int] = Field(None, example=8, description="Số session đã hoàn thành (integer)")
    completion_percentage: Optional[int] = Field(None, example=80, description="Phần trăm hoàn thành (0-100, integer)")
    is_achieved: Optional[int] = Field(None, example=1, description="Đã đạt được goal hay chưa: 0 = chưa, 1 = đã đạt (integer)")
    achieved_at: Optional[float] = Field(None, example=1703127056.789, description="Thời gian đạt được goal (Unix timestamp - float)")


class GoalBaseResponse(BaseModel):
    goal_id: int = Field(..., description="ID của goal (integer)")
    user_id: int = Field(..., description="ID của user sở hữu goal (integer)")
    goal_date: Optional[float] = Field(None, description="Ngày của goal (Unix timestamp - float)")
    target_sessions: Optional[int] = Field(None, description="Số session mục tiêu cần đạt (integer)")
    completed_sessions: Optional[int] = Field(None, description="Số session đã hoàn thành (integer)")
    completion_percentage: Optional[int] = Field(None, description="Phần trăm hoàn thành (0-100, integer)")
    is_achieved: Optional[int] = Field(None, description="Đã đạt được goal hay chưa: 0 = chưa, 1 = đã đạt (integer)")
    achieved_at: Optional[float] = Field(None, description="Thời gian đạt được goal (Unix timestamp - float)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

