from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class ShopCreateRequest(BaseModel):
    name: str = Field(..., example="Premium Theme", description="Tên của item trong shop (string)")
    price: float = Field(..., example=100.5, description="Giá của item (float, ví dụ: 100.5)")
    type: Optional[str] = Field(None, example="theme", description="Loại item (string)")


class ShopUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, example="Premium Theme", description="Tên của item trong shop (string)")
    price: Optional[float] = Field(None, example=120.0, description="Giá của item (float)")
    type: Optional[str] = Field(None, example="theme", description="Loại item (string)")


class ShopBaseResponse(BaseModel):
    shop_id: int = Field(..., description="ID của shop item (integer)")
    name: str = Field(..., description="Tên của item trong shop (string)")
    price: float = Field(..., description="Giá của item (float)")
    type: Optional[str] = Field(None, description="Loại item (string)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")


class ShopWithPurchaseStatusResponse(BaseModel):
    """Shop item with purchase status for current user"""
    shop_id: int = Field(..., description="ID của shop item (integer)")
    name: str = Field(..., description="Tên của item trong shop (string)")
    price: float = Field(..., description="Giá của item (float)")
    type: Optional[str] = Field(None, description="Loại item (string)")
    is_purchased: bool = Field(..., description="User hiện tại đã mua item này hay chưa: true = đã mua, false = chưa mua (boolean)")
    purchased_at: Optional[float] = Field(None, description="Thời gian mua item (Unix timestamp - float). Null nếu chưa mua")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")


class ShopPurchaseRequest(BaseModel):
    """Request to purchase a shop item"""
    pass  # No additional data needed, shop_id is in URL


class ShopPurchaseResponse(BaseModel):
    """Response after purchasing"""
    purchase_id: int = Field(..., description="ID của purchase record (integer)")
    user_id: int = Field(..., description="ID của user đã mua (integer)")
    shop_id: int = Field(..., description="ID của shop item đã mua (integer)")
    purchased_at: float = Field(..., description="Thời gian mua (Unix timestamp - float)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

