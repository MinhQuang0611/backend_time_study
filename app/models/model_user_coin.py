from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.model_base import Base, TimestampMixin


class UserCoinEntity(TimestampMixin, Base):
    """
    UserCoinEntity - Coin của User
    Bảng: user_coins
    """
    
    __tablename__ = "user_coins"
    
    coin_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    coin = Column(Integer, default=0, nullable=False)  # Số coin hiện tại
    
    # Relationships
    user = relationship("UserEntity", back_populates="user_coin")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_coins_user_id', 'user_id'),
    )

