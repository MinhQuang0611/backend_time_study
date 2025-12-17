from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schemas.sche_base import BaseModelResponse


class UserEntityCreateRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", description="Email của user (email string, ví dụ: user@example.com)")
    display_name: Optional[str] = Field(default=None, example="John Doe", max_length=255, description="Tên hiển thị của user (string, tối đa 255 ký tự)")
    profile_picture_url: Optional[str] = Field(default=None, example="https://example.com/avatar.jpg", max_length=1024, description="URL ảnh đại diện (string, tối đa 1024 ký tự)")
    is_anonymous: Optional[int] = Field(1, example=0, description="Là user ẩn danh hay không: 0 = không, 1 = có (integer, mặc định: 1)")
    last_login: Optional[float] = Field(None, example=1703123456.789, description="Thời gian đăng nhập lần cuối (Unix timestamp - float)")


class UserEntityUpdateRequest(BaseModel):
    email: Optional[EmailStr] = Field(None, example="user@example.com", description="Email của user (email string)")
    display_name: Optional[str] = Field(default=None, example="Jane Doe", max_length=255, description="Tên hiển thị của user (string, tối đa 255 ký tự)")
    profile_picture_url: Optional[str] = Field(default=None, example="https://example.com/avatar.jpg", max_length=1024, description="URL ảnh đại diện (string, tối đa 1024 ký tự)")
    is_anonymous: Optional[int] = Field(None, example=0, description="Là user ẩn danh hay không: 0 = không, 1 = có (integer)")
    last_login: Optional[float] = Field(None, example=1703123456.789, description="Thời gian đăng nhập lần cuối (Unix timestamp - float)")


class UserEntityBaseResponse(BaseModel):
    user_id: int = Field(..., description="ID của user (integer)")
    email: Optional[str] = Field(None, description="Email của user (string)")
    display_name: Optional[str] = Field(None, description="Tên hiển thị của user (string)")
    profile_picture_url: Optional[str] = Field(None, description="URL ảnh đại diện (string)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    last_login: Optional[float] = Field(None, description="Thời gian đăng nhập lần cuối (Unix timestamp - float)")
    is_anonymous: Optional[int] = Field(None, description="Là user ẩn danh hay không: 0 = không, 1 = có (integer)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

    class Config:
        from_attributes = True

