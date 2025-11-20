from typing import Optional
from pydantic import BaseModel
from app.schemas.sche_base import BaseModelResponse


class StatisticsCacheCreateRequest(BaseModel):
    user_id: int
    cache_date: float  # timestamp
    cache_type: str  # DAILY, MONTHLY, YEARLY
    total_sessions: Optional[int] = 0
    total_focus_time: Optional[int] = 0  # minutes
    total_break_time: Optional[int] = 0  # minutes
    completed_tasks: Optional[int] = 0
    goal_achieved: Optional[int] = 0
    current_streak: Optional[int] = 0
    best_streak: Optional[int] = 0


class StatisticsCacheUpdateRequest(BaseModel):
    cache_date: Optional[float] = None
    cache_type: Optional[str] = None
    total_sessions: Optional[int] = None
    total_focus_time: Optional[int] = None
    total_break_time: Optional[int] = None
    completed_tasks: Optional[int] = None
    goal_achieved: Optional[int] = None
    current_streak: Optional[int] = None
    best_streak: Optional[int] = None


class StatisticsCacheBaseResponse(BaseModel):
    cache_id: int
    user_id: int
    cache_date: Optional[float] = None
    cache_type: Optional[str] = None
    total_sessions: Optional[int] = None
    total_focus_time: Optional[int] = None
    total_break_time: Optional[int] = None
    completed_tasks: Optional[int] = None
    goal_achieved: Optional[int] = None
    current_streak: Optional[int] = None
    best_streak: Optional[int] = None
    cached_at: Optional[float] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class StreakRecordCreateRequest(BaseModel):
    user_id: int
    streak_date: float  # timestamp
    has_activity: Optional[int] = 0
    session_count: Optional[int] = 0
    focus_time: Optional[int] = 0  # minutes


class StreakRecordUpdateRequest(BaseModel):
    streak_date: Optional[float] = None
    has_activity: Optional[int] = None
    session_count: Optional[int] = None
    focus_time: Optional[int] = None


class StreakRecordBaseResponse(BaseModel):
    streak_id: int
    user_id: int
    streak_date: Optional[float] = None
    has_activity: Optional[int] = None
    session_count: Optional[int] = None
    focus_time: Optional[int] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

