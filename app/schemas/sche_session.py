from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class SessionCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    session_date: float = Field(..., example=1703123456.789, description="Ngày của session (Unix timestamp - float, ví dụ: 1703123456.789)")
    start_time: float = Field(..., example=1703123456.789, description="Thời gian bắt đầu session (Unix timestamp - float, ví dụ: 1703123456.789)")
    end_time: Optional[float] = Field(None, example=1703127056.789, description="Thời gian kết thúc session (Unix timestamp - float, ví dụ: 1703123456.789). Null nếu chưa kết thúc")
    duration_minutes: int = Field(..., example=25, description="Thời lượng dự kiến của session (phút - integer)")
    actual_duration_minutes: Optional[int] = Field(None, example=23, description="Thời lượng thực tế của session (phút - integer)")
    session_type: str = Field(..., example="FOCUS_SESSION", description="Loại session: 'FOCUS_SESSION', 'SHORT_BREAK', hoặc 'LONG_BREAK' (string)")
    status: Optional[str] = Field("IN_PROGRESS", example="IN_PROGRESS", description="Trạng thái session: 'IN_PROGRESS', 'COMPLETED', 'PAUSED', hoặc 'CANCELLED' (string)")
    focus_session_count: Optional[int] = Field(0, example=1, description="Số lượng focus session (integer, mặc định: 0)")
    is_completed: Optional[int] = Field(0, example=0, description="Đã hoàn thành hay chưa: 0 = chưa, 1 = đã hoàn thành (integer)")
    pause_count: Optional[int] = Field(0, example=0, description="Số lần tạm dừng (integer, mặc định: 0)")
    total_pause_duration: Optional[int] = Field(0, example=0, description="Tổng thời gian tạm dừng (phút - integer, mặc định: 0)")


class SessionUpdateRequest(BaseModel):
    session_date: Optional[float] = Field(None, example=1703123456.789, description="Ngày của session (Unix timestamp - float)")
    start_time: Optional[float] = Field(None, example=1703123456.789, description="Thời gian bắt đầu session (Unix timestamp - float)")
    end_time: Optional[float] = Field(None, example=1703127056.789, description="Thời gian kết thúc session (Unix timestamp - float)")
    duration_minutes: Optional[int] = Field(None, example=25, description="Thời lượng dự kiến của session (phút - integer)")
    actual_duration_minutes: Optional[int] = Field(None, example=23, description="Thời lượng thực tế của session (phút - integer)")
    session_type: Optional[str] = Field(None, example="FOCUS_SESSION", description="Loại session: 'FOCUS_SESSION', 'SHORT_BREAK', hoặc 'LONG_BREAK'")
    status: Optional[str] = Field(None, example="COMPLETED", description="Trạng thái session: 'IN_PROGRESS', 'COMPLETED', 'PAUSED', hoặc 'CANCELLED'")
    focus_session_count: Optional[int] = Field(None, example=1, description="Số lượng focus session (integer)")
    is_completed: Optional[int] = Field(None, example=1, description="Đã hoàn thành hay chưa: 0 = chưa, 1 = đã hoàn thành (integer)")
    pause_count: Optional[int] = Field(None, example=2, description="Số lần tạm dừng (integer)")
    total_pause_duration: Optional[int] = Field(None, example=5, description="Tổng thời gian tạm dừng (phút - integer)")


class SessionBaseResponse(BaseModel):
    session_id: int = Field(..., description="ID của session (integer)")
    user_id: int = Field(..., description="ID của user sở hữu session (integer)")
    session_date: Optional[float] = Field(None, description="Ngày của session (Unix timestamp - float)")
    start_time: Optional[float] = Field(None, description="Thời gian bắt đầu session (Unix timestamp - float)")
    end_time: Optional[float] = Field(None, description="Thời gian kết thúc session (Unix timestamp - float)")
    duration_minutes: Optional[int] = Field(None, description="Thời lượng dự kiến của session (phút - integer)")
    actual_duration_minutes: Optional[int] = Field(None, description="Thời lượng thực tế của session (phút - integer)")
    session_type: Optional[str] = Field(None, description="Loại session: 'FOCUS_SESSION', 'SHORT_BREAK', hoặc 'LONG_BREAK' (string)")
    status: Optional[str] = Field(None, description="Trạng thái session: 'IN_PROGRESS', 'COMPLETED', 'PAUSED', hoặc 'CANCELLED' (string)")
    focus_session_count: Optional[int] = Field(None, description="Số lượng focus session (integer)")
    is_completed: Optional[int] = Field(None, description="Đã hoàn thành hay chưa: 0 = chưa, 1 = đã hoàn thành (integer)")
    pause_count: Optional[int] = Field(None, description="Số lần tạm dừng (integer)")
    total_pause_duration: Optional[int] = Field(None, description="Tổng thời gian tạm dừng (phút - integer)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")


class SessionPauseCreateRequest(BaseModel):
    session_id: int = Field(..., example=1, description="ID của session (integer)")
    pause_start: float = Field(..., example=1703123456.789, description="Thời gian bắt đầu tạm dừng (Unix timestamp - float, ví dụ: 1703123456.789)")
    pause_end: Optional[float] = Field(None, example=1703123556.789, description="Thời gian kết thúc tạm dừng (Unix timestamp - float). Null nếu chưa kết thúc")
    pause_duration: Optional[int] = Field(None, example=2, description="Thời lượng tạm dừng (phút - integer)")


class SessionPauseUpdateRequest(BaseModel):
    pause_start: Optional[float] = Field(None, example=1703123456.789, description="Thời gian bắt đầu tạm dừng (Unix timestamp - float)")
    pause_end: Optional[float] = Field(None, example=1703123556.789, description="Thời gian kết thúc tạm dừng (Unix timestamp - float)")
    pause_duration: Optional[int] = Field(None, example=2, description="Thời lượng tạm dừng (phút - integer)")


class SessionPauseBaseResponse(BaseModel):
    pause_id: int = Field(..., description="ID của pause (integer)")
    session_id: int = Field(..., description="ID của session (integer)")
    pause_start: Optional[float] = Field(None, description="Thời gian bắt đầu tạm dừng (Unix timestamp - float)")
    pause_end: Optional[float] = Field(None, description="Thời gian kết thúc tạm dừng (Unix timestamp - float)")
    pause_duration: Optional[int] = Field(None, description="Thời lượng tạm dừng (phút - integer)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

