from typing import Optional
from pydantic import BaseModel
from app.schemas.sche_base import BaseModelResponse


class ShopCreateRequest(BaseModel):
    name: str
    price: float
    type: Optional[str] = None


class ShopUpdateRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    type: Optional[str] = None


class ShopBaseResponse(BaseModel):
    shop_id: int
    name: str
    price: float
    type: Optional[str] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class ShopWithPurchaseStatusResponse(BaseModel):
    """Shop item with purchase status for current user"""
    shop_id: int
    name: str
    price: float
    type: Optional[str] = None
    is_purchased: bool  # True if current user has purchased this item
    purchased_at: Optional[float] = None  # timestamp when purchased (if purchased)
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class ShopPurchaseRequest(BaseModel):
    """Request to purchase a shop item"""
    pass  # No additional data needed, shop_id is in URL


class ShopPurchaseResponse(BaseModel):
    """Response after purchasing"""
    purchase_id: int
    user_id: int
    shop_id: int
    purchased_at: float
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

