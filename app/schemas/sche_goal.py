from typing import Optional
from pydantic import BaseModel
from app.schemas.sche_base import BaseModelResponse


class GoalCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    goal_date: float  # timestamp
    target_sessions: int
    completed_sessions: Optional[int] = 0
    completion_percentage: Optional[int] = 0
    is_achieved: Optional[int] = 0
    achieved_at: Optional[float] = None  # timestamp


class GoalUpdateRequest(BaseModel):
    goal_date: Optional[float] = None
    target_sessions: Optional[int] = None
    completed_sessions: Optional[int] = None
    completion_percentage: Optional[int] = None
    is_achieved: Optional[int] = None
    achieved_at: Optional[float] = None


class GoalBaseResponse(BaseModel):
    goal_id: int
    user_id: int
    goal_date: Optional[float] = None
    target_sessions: Optional[int] = None
    completed_sessions: Optional[int] = None
    completion_percentage: Optional[int] = None
    is_achieved: Optional[int] = None
    achieved_at: Optional[float] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

