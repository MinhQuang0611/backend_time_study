from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class TaskEntity(TimestampMixin, Base):
    """
    TaskEntity - Quản Lý Nhiệm Vụ
    Bảng: tasks
    """
    
    __tablename__ = "tasks"
    
    # Constants
    PRIORITY_HIGH = "HIGH"
    PRIORITY_MEDIUM = "MEDIUM"
    PRIORITY_LOW = "LOW"
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String)
    description = Column(String)
    priority = Column(String, default=PRIORITY_MEDIUM)
    task_date = Column(Float)  # timestamp
    is_completed = Column(Integer, default=0)
    completed_at = Column(Float, nullable=True)  # timestamp
    total_time_spent = Column(Integer, default=0)  # minutes
    estimated_sessions = Column(Integer, default=1)
    actual_sessions = Column(Integer, default=0)
    order_index = Column(Integer, default=0)
    
    # Relationships
    user = relationship("UserEntity", back_populates="tasks")
    task_sessions = relationship("TaskSessionEntity", back_populates="task", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_tasks_user_id', 'user_id'),
        Index('idx_tasks_task_date', 'task_date'),
        Index('idx_tasks_user_date', 'user_id', 'task_date'),
        Index('idx_tasks_priority', 'priority'),
        Index('idx_tasks_is_completed', 'is_completed'),
    )


class TaskSessionEntity(TimestampMixin, Base):
    """
    TaskSessionEntity - Liên Kết Task-Session
    Bảng: task_sessions
    """
    
    __tablename__ = "task_sessions"
    
    task_session_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)
    time_spent = Column(Integer)  # minutes
    notes = Column(String)
    
    # Relationships
    task = relationship("TaskEntity", back_populates="task_sessions")
    session = relationship("SessionEntity", back_populates="task_sessions")

