from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.config import settings


class UserEntityRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: Optional[str] = Field(default=None, max_length=255)
    profile_picture_url: Optional[str] = Field(default=None, max_length=1024)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value.isnumeric():
            raise ValueError("Password must contain non-numeric characters")
        return value


class UserEntityLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserEntityTokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[float] = settings.ACCESS_TOKEN_EXPIRE_SECONDS
    refresh_expires_in: Optional[float] = settings.ACCESS_TOKEN_EXPIRE_SECONDS
    token_type: Optional[str] = "Bearer"
    user: Optional[dict] = None  # User info


class FirebaseLoginRequest(BaseModel):
    firebase_id_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

