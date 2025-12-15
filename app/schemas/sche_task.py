from typing import Optional
from pydantic import BaseModel
from app.schemas.sche_base import BaseModelResponse


class TaskCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "MEDIUM"  # HIGH, MEDIUM, LOW
    task_date: float  # timestamp
    is_completed: Optional[int] = 0
    completed_at: Optional[float] = None  # timestamp
    total_time_spent: Optional[int] = 0  # minutes
    estimated_sessions: Optional[int] = 1
    actual_sessions: Optional[int] = 0
    order_index: Optional[int] = 0


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    task_date: Optional[float] = None
    is_completed: Optional[int] = None
    completed_at: Optional[float] = None
    total_time_spent: Optional[int] = None
    estimated_sessions: Optional[int] = None
    actual_sessions: Optional[int] = None
    order_index: Optional[int] = None


class TaskBaseResponse(BaseModel):
    task_id: int
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    task_date: Optional[float] = None
    is_completed: Optional[int] = None
    completed_at: Optional[float] = None
    total_time_spent: Optional[int] = None
    estimated_sessions: Optional[int] = None
    actual_sessions: Optional[int] = None
    order_index: Optional[int] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class TaskSessionCreateRequest(BaseModel):
    task_id: int
    session_id: int
    time_spent: int  # minutes
    notes: Optional[str] = None


class TaskSessionUpdateRequest(BaseModel):
    task_id: Optional[int] = None
    session_id: Optional[int] = None
    time_spent: Optional[int] = None
    notes: Optional[str] = None


class TaskSessionBaseResponse(BaseModel):
    task_session_id: int
    task_id: int
    session_id: int
    time_spent: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

