from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class UserSettingEntity(TimestampMixin, Base):
    """
    UserSettingEntity - Cài Đặt Cá Nhân
    Bảng: user_settings
    """
    
    __tablename__ = "user_settings"
    
    # Constants
    TYPE_STRING = "STRING"
    TYPE_INTEGER = "INTEGER"
    TYPE_BOOLEAN = "BOOLEAN"
    TYPE_JSON = "JSON"
    
    setting_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    setting_key = Column(String, nullable=False)
    setting_value = Column(String)
    data_type = Column(String, default=TYPE_STRING)
    
    # Relationships
    user = relationship("UserEntity", back_populates="settings")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'setting_key', name='uq_user_settings_user_key'),
    )


class DefaultSettingEntity(TimestampMixin, Base):
    """
    DefaultSettingEntity - Cài Đặt Mặc Định
    Bảng: default_settings
    """
    
    __tablename__ = "default_settings"
    
    # Constants
    CATEGORY_TIMER = "TIMER"
    CATEGORY_NOTIFICATION = "NOTIFICATION"
    CATEGORY_APPEARANCE = "APPEARANCE"
    CATEGORY_DATA = "DATA"
    
    default_setting_id = Column(Integer, primary_key=True, autoincrement=True)
    setting_key = Column(String, unique=True, nullable=False)
    default_value = Column(String)
    data_type = Column(String)
    category = Column(String, index=True)
    description = Column(String)
    is_configurable = Column(Integer, default=1)
    
    # Indexes
    __table_args__ = (
        Index('idx_default_settings_category', 'category'),
    )

