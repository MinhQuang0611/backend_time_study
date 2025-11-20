from typing import Optional
from pydantic import BaseModel
from app.schemas.sche_base import BaseModelResponse


class SessionCreateRequest(BaseModel):
    user_id: int
    session_date: float  # timestamp
    start_time: float  # timestamp
    end_time: Optional[float] = None  # timestamp
    duration_minutes: int
    actual_duration_minutes: Optional[int] = None
    session_type: str  # FOCUS_SESSION, SHORT_BREAK, LONG_BREAK
    status: Optional[str] = "IN_PROGRESS"  # IN_PROGRESS, COMPLETED, PAUSED, CANCELLED
    focus_session_count: Optional[int] = 0
    is_completed: Optional[int] = 0
    pause_count: Optional[int] = 0
    total_pause_duration: Optional[int] = 0


class SessionUpdateRequest(BaseModel):
    session_date: Optional[float] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration_minutes: Optional[int] = None
    actual_duration_minutes: Optional[int] = None
    session_type: Optional[str] = None
    status: Optional[str] = None
    focus_session_count: Optional[int] = None
    is_completed: Optional[int] = None
    pause_count: Optional[int] = None
    total_pause_duration: Optional[int] = None


class SessionBaseResponse(BaseModel):
    session_id: int
    user_id: int
    session_date: Optional[float] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration_minutes: Optional[int] = None
    actual_duration_minutes: Optional[int] = None
    session_type: Optional[str] = None
    status: Optional[str] = None
    focus_session_count: Optional[int] = None
    is_completed: Optional[int] = None
    pause_count: Optional[int] = None
    total_pause_duration: Optional[int] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class SessionPauseCreateRequest(BaseModel):
    session_id: int
    pause_start: float  # timestamp
    pause_end: Optional[float] = None  # timestamp
    pause_duration: Optional[int] = None  # minutes


class SessionPauseUpdateRequest(BaseModel):
    pause_start: Optional[float] = None
    pause_end: Optional[float] = None
    pause_duration: Optional[int] = None


class SessionPauseBaseResponse(BaseModel):
    pause_id: int
    session_id: int
    pause_start: Optional[float] = None
    pause_end: Optional[float] = None
    pause_duration: Optional[int] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

