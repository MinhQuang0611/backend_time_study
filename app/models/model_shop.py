from sqlalchemy import Column, Integer, String, Float, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.models.model_base import Base, TimestampMixin


class ShopEntity(TimestampMixin, Base):
    """
    ShopEntity - Quản Lý Sản Phẩm Cửa Hàng
    Bảng: shop
    Lưu thông tin sản phẩm, không chia theo user
    """
    
    __tablename__ = "shop"
    
    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    type = Column(String, nullable=True)  # Type of shop item (theme, avatar, pack, etc.)
    
    # Relationships
    purchases = relationship("ShopPurchaseEntity", back_populates="shop", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_shop_type', 'type'),
    )


class ShopPurchaseEntity(TimestampMixin, Base):
    """
    ShopPurchaseEntity - Lưu Trạng Thái Mua Hàng Của User
    Bảng: shop_purchases
    Mỗi user có trạng thái mua riêng cho từng sản phẩm
    """
    
    __tablename__ = "shop_purchases"
    
    purchase_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.shop_id", ondelete="CASCADE"), nullable=False)
    purchased_at = Column(Float, nullable=False)  # timestamp when purchased
    
    # Relationships
    user = relationship("UserEntity", back_populates="shop_purchases")
    shop = relationship("ShopEntity", back_populates="purchases")
    
    # Indexes - Unique constraint: một user chỉ mua một sản phẩm một lần
    __table_args__ = (
        Index('idx_shop_purchases_user_id', 'user_id'),
        Index('idx_shop_purchases_shop_id', 'shop_id'),
        Index('idx_shop_purchases_user_shop', 'user_id', 'shop_id', unique=True),
    )

