from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class SessionEntity(TimestampMixin, Base):
    """
    SessionEntity - Phiên Học Tập
    Bảng: sessions
    """
    
    __tablename__ = "sessions"
    
    # Constants
    TYPE_FOCUS_SESSION = "FOCUS_SESSION"
    TYPE_SHORT_BREAK = "SHORT_BREAK"
    TYPE_LONG_BREAK = "LONG_BREAK"
    
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PAUSED = "PAUSED"
    STATUS_CANCELLED = "CANCELLED"
    
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    session_date = Column(Float)  # timestamp
    start_time = Column(Float)  # timestamp
    end_time = Column(Float)  # timestamp
    duration_minutes = Column(Integer)
    actual_duration_minutes = Column(Integer, nullable=True)
    session_type = Column(String, index=True)
    status = Column(String, default=STATUS_IN_PROGRESS)
    focus_session_count = Column(Integer, default=0)
    is_completed = Column(Integer, default=0)
    pause_count = Column(Integer, default=0)
    total_pause_duration = Column(Integer, default=0)
    
    # Relationships
    user = relationship("UserEntity", back_populates="sessions")
    pauses = relationship("SessionPauseEntity", back_populates="session", cascade="all, delete-orphan")
    task_sessions = relationship("TaskSessionEntity", back_populates="session", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_sessions_user_id', 'user_id'),
        Index('idx_sessions_session_date', 'session_date'),
        Index('idx_sessions_user_date', 'user_id', 'session_date'),
        Index('idx_sessions_session_type', 'session_type'),
        Index('idx_sessions_status', 'status'),
    )


class SessionPauseEntity(TimestampMixin, Base):
    """
    SessionPauseEntity - Tạm Dừng Session
    Bảng: session_pauses
    """
    
    __tablename__ = "session_pauses"
    
    pause_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)
    pause_start = Column(Float)  # timestamp
    pause_end = Column(Float)  # timestamp
    pause_duration = Column(Integer, nullable=True)  # minutes
    
    # Relationships
    session = relationship("SessionEntity", back_populates="pauses")

