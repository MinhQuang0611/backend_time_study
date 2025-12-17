from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class StatisticsCacheCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    cache_date: float = Field(..., example=1703123456.789, description="Ngày của cache (Unix timestamp - float, ví dụ: 1703123456.789)")
    cache_type: str = Field(..., example="DAILY", description="Loại cache: 'DAILY', 'MONTHLY', hoặc 'YEARLY' (string)")
    total_sessions: Optional[int] = Field(0, example=5, description="Tổng số session (integer, mặc định: 0)")
    total_focus_time: Optional[int] = Field(0, example=125, description="Tổng thời gian focus (phút - integer, mặc định: 0)")
    total_break_time: Optional[int] = Field(0, example=30, description="Tổng thời gian nghỉ (phút - integer, mặc định: 0)")
    completed_tasks: Optional[int] = Field(0, example=3, description="Số task đã hoàn thành (integer, mặc định: 0)")
    goal_achieved: Optional[int] = Field(0, example=1, description="Số goal đã đạt được (integer, mặc định: 0)")
    current_streak: Optional[int] = Field(0, example=7, description="Chuỗi ngày hiện tại (integer, mặc định: 0)")
    best_streak: Optional[int] = Field(0, example=15, description="Chuỗi ngày tốt nhất (integer, mặc định: 0)")


class StatisticsCacheUpdateRequest(BaseModel):
    cache_date: Optional[float] = Field(None, example=1703123456.789, description="Ngày của cache (Unix timestamp - float)")
    cache_type: Optional[str] = Field(None, example="DAILY", description="Loại cache: 'DAILY', 'MONTHLY', hoặc 'YEARLY'")
    total_sessions: Optional[int] = Field(None, example=5, description="Tổng số session (integer)")
    total_focus_time: Optional[int] = Field(None, example=125, description="Tổng thời gian focus (phút - integer)")
    total_break_time: Optional[int] = Field(None, example=30, description="Tổng thời gian nghỉ (phút - integer)")
    completed_tasks: Optional[int] = Field(None, example=3, description="Số task đã hoàn thành (integer)")
    goal_achieved: Optional[int] = Field(None, example=1, description="Số goal đã đạt được (integer)")
    current_streak: Optional[int] = Field(None, example=7, description="Chuỗi ngày hiện tại (integer)")
    best_streak: Optional[int] = Field(None, example=15, description="Chuỗi ngày tốt nhất (integer)")


class StatisticsCacheBaseResponse(BaseModel):
    cache_id: int = Field(..., description="ID của cache (integer)")
    user_id: int = Field(..., description="ID của user sở hữu cache (integer)")
    cache_date: Optional[float] = Field(None, description="Ngày của cache (Unix timestamp - float)")
    cache_type: Optional[str] = Field(None, description="Loại cache: 'DAILY', 'MONTHLY', hoặc 'YEARLY' (string)")
    total_sessions: Optional[int] = Field(None, description="Tổng số session (integer)")
    total_focus_time: Optional[int] = Field(None, description="Tổng thời gian focus (phút - integer)")
    total_break_time: Optional[int] = Field(None, description="Tổng thời gian nghỉ (phút - integer)")
    completed_tasks: Optional[int] = Field(None, description="Số task đã hoàn thành (integer)")
    goal_achieved: Optional[int] = Field(None, description="Số goal đã đạt được (integer)")
    current_streak: Optional[int] = Field(None, description="Chuỗi ngày hiện tại (integer)")
    best_streak: Optional[int] = Field(None, description="Chuỗi ngày tốt nhất (integer)")
    cached_at: Optional[float] = Field(None, description="Thời gian cache (Unix timestamp - float)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")


class StreakRecordCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    streak_date: float = Field(..., example=1703123456.789, description="Ngày của streak record (Unix timestamp - float, ví dụ: 1703123456.789)")
    has_activity: Optional[int] = Field(0, example=1, description="Có hoạt động hay không: 0 = không, 1 = có (integer, mặc định: 0)")
    session_count: Optional[int] = Field(0, example=3, description="Số session trong ngày (integer, mặc định: 0)")
    focus_time: Optional[int] = Field(0, example=75, description="Thời gian focus trong ngày (phút - integer, mặc định: 0)")


class StreakRecordUpdateRequest(BaseModel):
    streak_date: Optional[float] = Field(None, example=1703123456.789, description="Ngày của streak record (Unix timestamp - float)")
    has_activity: Optional[int] = Field(None, example=1, description="Có hoạt động hay không: 0 = không, 1 = có (integer)")
    session_count: Optional[int] = Field(None, example=3, description="Số session trong ngày (integer)")
    focus_time: Optional[int] = Field(None, example=75, description="Thời gian focus trong ngày (phút - integer)")


class StreakRecordBaseResponse(BaseModel):
    streak_id: int = Field(..., description="ID của streak record (integer)")
    user_id: int = Field(..., description="ID của user sở hữu streak record (integer)")
    streak_date: Optional[float] = Field(None, description="Ngày của streak record (Unix timestamp - float)")
    has_activity: Optional[int] = Field(None, description="Có hoạt động hay không: 0 = không, 1 = có (integer)")
    session_count: Optional[int] = Field(None, description="Số session trong ngày (integer)")
    focus_time: Optional[int] = Field(None, description="Thời gian focus trong ngày (phút - integer)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

