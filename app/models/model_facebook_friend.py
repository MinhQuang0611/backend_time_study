from sqlalchemy import Column, Integer, String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.model_base import TimestampMixin, Base


class FacebookFriend(TimestampMixin, Base):
    """
    FacebookFriend - Danh sách bạn bè Facebook
    Bảng: facebook_friends
    """
    
    __tablename__ = "facebook_friends"
    
    friend_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    facebook_user_id = Column(String, nullable=False, index=True)  # Facebook ID của bạn bè
    name = Column(String)  # Tên bạn bè
    picture_url = Column(String)  # URL ảnh đại diện
    
    # Relationships
    user = relationship("UserEntity", back_populates="facebook_friends")
    
    # Indexes và constraints
    __table_args__ = (
        UniqueConstraint("user_id", "facebook_user_id", name="uq_user_facebook_friend"),
        Index('idx_facebook_friends_user_id', 'user_id'),
        Index('idx_facebook_friends_facebook_user_id', 'facebook_user_id'),
    )

