from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class TaskCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    title: str = Field(..., example="Hoàn thành dự án ABC", description="Tiêu đề của task (string)")
    description: Optional[str] = Field(None, example="Làm xong tính năng XYZ và test", description="Mô tả chi tiết của task (string)")
    priority: Optional[str] = Field("MEDIUM", example="HIGH", description="Độ ưu tiên: 'HIGH', 'MEDIUM', hoặc 'LOW' (string, mặc định: 'MEDIUM')")
    task_date: float = Field(..., example=1703123456.789, description="Ngày của task (Unix timestamp - float, ví dụ: 1703123456.789)")
    is_completed: Optional[int] = Field(0, example=0, description="Đã hoàn thành hay chưa: 0 = chưa, 1 = đã hoàn thành (integer, mặc định: 0)")
    completed_at: Optional[float] = Field(None, example=1703127056.789, description="Thời gian hoàn thành task (Unix timestamp - float). Null nếu chưa hoàn thành")
    total_time_spent: Optional[int] = Field(0, example=120, description="Tổng thời gian đã dùng cho task (phút - integer, mặc định: 0)")
    estimated_sessions: Optional[int] = Field(1, example=5, description="Số session dự kiến để hoàn thành task (integer, mặc định: 1)")
    actual_sessions: Optional[int] = Field(0, example=3, description="Số session thực tế đã dùng (integer, mặc định: 0)")
    order_index: Optional[int] = Field(0, example=1, description="Thứ tự sắp xếp của task (integer, mặc định: 0)")


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, example="Tiêu đề mới", description="Tiêu đề của task (string)")
    description: Optional[str] = Field(None, example="Mô tả mới", description="Mô tả chi tiết của task (string)")
    priority: Optional[str] = Field(None, example="MEDIUM", description="Độ ưu tiên: 'HIGH', 'MEDIUM', hoặc 'LOW' (string)")
    task_date: Optional[float] = Field(None, example=1703123456.789, description="Ngày của task (Unix timestamp - float)")
    is_completed: Optional[int] = Field(None, example=1, description="Đã hoàn thành hay chưa: 0 = chưa, 1 = đã hoàn thành (integer)")
    completed_at: Optional[float] = Field(None, example=1703127056.789, description="Thời gian hoàn thành task (Unix timestamp - float)")
    total_time_spent: Optional[int] = Field(None, example=120, description="Tổng thời gian đã dùng cho task (phút - integer)")
    estimated_sessions: Optional[int] = Field(None, example=5, description="Số session dự kiến để hoàn thành task (integer)")
    actual_sessions: Optional[int] = Field(None, example=3, description="Số session thực tế đã dùng (integer)")
    order_index: Optional[int] = Field(None, example=1, description="Thứ tự sắp xếp của task (integer)")


class TaskBaseResponse(BaseModel):
    task_id: int = Field(..., description="ID của task (integer)")
    user_id: int = Field(..., description="ID của user sở hữu task (integer)")
    title: Optional[str] = Field(None, description="Tiêu đề của task (string)")
    description: Optional[str] = Field(None, description="Mô tả chi tiết của task (string)")
    priority: Optional[str] = Field(None, description="Độ ưu tiên: 'HIGH', 'MEDIUM', hoặc 'LOW' (string)")
    task_date: Optional[float] = Field(None, description="Ngày của task (Unix timestamp - float)")
    is_completed: Optional[int] = Field(None, description="Đã hoàn thành hay chưa: 0 = chưa, 1 = đã hoàn thành (integer)")
    completed_at: Optional[float] = Field(None, description="Thời gian hoàn thành task (Unix timestamp - float)")
    total_time_spent: Optional[int] = Field(None, description="Tổng thời gian đã dùng cho task (phút - integer)")
    estimated_sessions: Optional[int] = Field(None, description="Số session dự kiến để hoàn thành task (integer)")
    actual_sessions: Optional[int] = Field(None, description="Số session thực tế đã dùng (integer)")
    order_index: Optional[int] = Field(None, description="Thứ tự sắp xếp của task (integer)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")


class TaskSessionCreateRequest(BaseModel):
    task_id: int = Field(..., example=1, description="ID của task (integer)")
    session_id: int = Field(..., example=1, description="ID của session (integer)")
    time_spent: int = Field(..., example=25, description="Thời gian đã dùng cho task trong session này (phút - integer)")
    notes: Optional[str] = Field(None, example="Hoàn thành task A", description="Ghi chú về task session (string)")


class TaskSessionUpdateRequest(BaseModel):
    task_id: Optional[int] = Field(None, example=1, description="ID của task (integer)")
    session_id: Optional[int] = Field(None, example=1, description="ID của session (integer)")
    time_spent: Optional[int] = Field(None, example=25, description="Thời gian đã dùng cho task trong session này (phút - integer)")
    notes: Optional[str] = Field(None, example="Cập nhật ghi chú", description="Ghi chú về task session (string)")


class TaskSessionBaseResponse(BaseModel):
    task_session_id: int = Field(..., description="ID của task session (integer)")
    task_id: int = Field(..., description="ID của task (integer)")
    session_id: int = Field(..., description="ID của session (integer)")
    time_spent: Optional[int] = Field(None, description="Thời gian đã dùng cho task trong session này (phút - integer)")
    notes: Optional[str] = Field(None, description="Ghi chú về task session (string)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

