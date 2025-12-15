from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class UserEntity(TimestampMixin, Base):
    """
    UserEntity - Quản Lý Người Dùng
    Bảng: users
    """
    
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    display_name = Column(String)
    profile_picture_url = Column(String)
    hashed_password = Column(String(255), nullable=True)  # For authentication
    last_login = Column(Float, nullable=True)  # timestamp
    is_anonymous = Column(Integer, default=1)
    # created_at and updated_at are inherited from BareBaseModel
    
    # Relationships
    sessions = relationship("SessionEntity", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("TaskEntity", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("GoalEntity", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettingEntity", back_populates="user", cascade="all, delete-orphan")
    statistics_cache = relationship("StatisticsCacheEntity", back_populates="user", cascade="all, delete-orphan")
    streak_records = relationship("StreakRecordEntity", back_populates="user", cascade="all, delete-orphan")
    shop_purchases = relationship("ShopPurchaseEntity", back_populates="user", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_created_at', 'created_at'),
    )

