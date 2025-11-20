from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schemas.sche_base import BaseModelResponse


class UserEntityCreateRequest(BaseModel):
    email: EmailStr
    display_name: Optional[str] = Field(default=None, max_length=255)
    profile_picture_url: Optional[str] = Field(default=None, max_length=1024)
    is_anonymous: Optional[int] = 1
    last_login: Optional[float] = None  # timestamp


class UserEntityUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = Field(default=None, max_length=255)
    profile_picture_url: Optional[str] = Field(default=None, max_length=1024)
    is_anonymous: Optional[int] = None
    last_login: Optional[float] = None


class UserEntityBaseResponse(BaseModel):
    user_id: int
    email: Optional[str] = None
    display_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: Optional[float] = None
    last_login: Optional[float] = None
    is_anonymous: Optional[int] = None
    updated_at: Optional[float] = None

    class Config:
        from_attributes = True

