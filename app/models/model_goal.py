from sqlalchemy import Column, Integer, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class GoalEntity(TimestampMixin, Base):
    """
    GoalEntity - Mục Tiêu Hàng Ngày
    Bảng: goals
    """
    
    __tablename__ = "goals"
    
    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    goal_date = Column(Float)  # timestamp
    target_sessions = Column(Integer)
    completed_sessions = Column(Integer, default=0)
    completion_percentage = Column(Integer, default=0)
    is_achieved = Column(Integer, default=0)
    achieved_at = Column(Float, nullable=True)  # timestamp
    # created_at and updated_at are inherited from BareBaseModel
    
    # Relationships
    user = relationship("UserEntity", back_populates="goals")
    
    # Indexes and Constraints
    __table_args__ = (
        Index('idx_goals_user_id', 'user_id'),
        Index('idx_goals_goal_date', 'goal_date'),
        UniqueConstraint('user_id', 'goal_date', name='uq_goals_user_date'),
    )

