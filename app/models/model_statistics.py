from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class StatisticsCacheEntity(TimestampMixin, Base):
    """
    StatisticsCacheEntity - Cache Thống Kê
    Bảng: statistics_cache
    """
    
    __tablename__ = "statistics_cache"
    
    # Constants
    TYPE_DAILY = "DAILY"
    TYPE_MONTHLY = "MONTHLY"
    TYPE_YEARLY = "YEARLY"
    
    cache_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    cache_date = Column(Float)  # timestamp
    cache_type = Column(String, nullable=False)
    total_sessions = Column(Integer, default=0)
    total_focus_time = Column(Integer, default=0)  # minutes
    total_break_time = Column(Integer, default=0)  # minutes
    completed_tasks = Column(Integer, default=0)
    goal_achieved = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    cached_at = Column(Float)  # timestamp
    
    # Relationships
    user = relationship("UserEntity", back_populates="statistics_cache")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'cache_date', 'cache_type', name='uq_statistics_cache_user_date_type'),
    )


class StreakRecordEntity(TimestampMixin, Base):
    """
    StreakRecordEntity - Theo Dõi Chuỗi
    Bảng: streak_records
    """
    
    __tablename__ = "streak_records"
    
    streak_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    streak_date = Column(Float)  # timestamp
    has_activity = Column(Integer, default=0)
    session_count = Column(Integer, default=0)
    focus_time = Column(Integer, default=0)  # minutes
    
    # Relationships
    user = relationship("UserEntity", back_populates="streak_records")

