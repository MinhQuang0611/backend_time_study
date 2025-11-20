from typing import Optional
from pydantic import BaseModel
from app.schemas.sche_base import BaseModelResponse


class UserSettingCreateRequest(BaseModel):
    user_id: int
    setting_key: str
    setting_value: Optional[str] = None
    data_type: Optional[str] = "STRING"  # STRING, INTEGER, BOOLEAN, JSON


class UserSettingUpdateRequest(BaseModel):
    setting_key: Optional[str] = None
    setting_value: Optional[str] = None
    data_type: Optional[str] = None


class UserSettingBaseResponse(BaseModel):
    setting_id: int
    user_id: int
    setting_key: Optional[str] = None
    setting_value: Optional[str] = None
    data_type: Optional[str] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None


class DefaultSettingCreateRequest(BaseModel):
    setting_key: str
    default_value: Optional[str] = None
    data_type: Optional[str] = None
    category: Optional[str] = None  # TIMER, NOTIFICATION, APPEARANCE, DATA
    description: Optional[str] = None
    is_configurable: Optional[int] = 1


class DefaultSettingUpdateRequest(BaseModel):
    setting_key: Optional[str] = None
    default_value: Optional[str] = None
    data_type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_configurable: Optional[int] = None


class DefaultSettingBaseResponse(BaseModel):
    default_setting_id: int
    setting_key: Optional[str] = None
    default_value: Optional[str] = None
    data_type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_configurable: Optional[int] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

