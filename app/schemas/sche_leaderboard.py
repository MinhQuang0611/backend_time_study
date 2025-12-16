from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class LeaderboardPeriod(str, Enum):
    """Period cho leaderboard"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"


class LeaderboardMetric(str, Enum):
    """Metric để sort leaderboard"""
    FOCUS_TIME = "focus_time"  # Tổng thời gian focus (minutes)
    SESSIONS = "sessions"  # Tổng số sessions
    TASKS = "tasks"  # Số tasks hoàn thành
    STREAK = "streak"  # Current streak
    BEST_STREAK = "best_streak"  # Best streak
    GOALS = "goals"  # Số goals đạt được


class LeaderboardEntry(BaseModel):
    """Một entry trong leaderboard"""
    rank: int
    user_id: int
    display_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    facebook_user_id: Optional[str] = None  # Facebook ID nếu là bạn bè
    is_current_user: bool = False
    
    # Metrics
    focus_time: int = 0  # minutes
    sessions: int = 0
    tasks: int = 0
    current_streak: int = 0
    best_streak: int = 0
    goals: int = 0
    
    # Score (tổng điểm dựa trên metric được chọn)
    score: float = 0.0


class LeaderboardResponse(BaseModel):
    """Response cho leaderboard"""
    period: str
    metric: str
    current_user_rank: Optional[int] = None
    total_participants: int
    entries: List[LeaderboardEntry]
    note: Optional[str] = None


class LeaderboardRequest(BaseModel):
    """Request cho leaderboard"""
    period: LeaderboardPeriod = Field(
        default=LeaderboardPeriod.ALL_TIME,
        description="Period: daily, weekly, monthly, all_time"
    )
    metric: LeaderboardMetric = Field(
        default=LeaderboardMetric.FOCUS_TIME,
        description="Metric để sort: focus_time, sessions, tasks, streak, best_streak, goals"
    )
    limit: Optional[int] = Field(
        default=50,
        ge=1,
        le=100,
        description="Số lượng entries trả về (1-100)"
    )
    include_self: bool = Field(
        default=True,
        description="Có bao gồm current user trong leaderboard không"
    )

