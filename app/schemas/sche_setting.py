from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.sche_base import BaseModelResponse


class UserSettingCreateRequest(BaseModel):
    # user_id is now obtained from JWT token
    setting_key: str = Field(..., example="focus_duration", description="Khóa của setting (string)")
    setting_value: Optional[str] = Field(None, example="25", description="Giá trị của setting (string)")
    data_type: Optional[str] = Field("STRING", example="STRING", description="Kiểu dữ liệu: 'STRING', 'INTEGER', 'BOOLEAN', hoặc 'JSON' (string, mặc định: 'STRING')")


class UserSettingUpdateRequest(BaseModel):
    setting_key: Optional[str] = Field(None, example="focus_duration", description="Khóa của setting (string)")
    setting_value: Optional[str] = Field(None, example="30", description="Giá trị của setting (string)")
    data_type: Optional[str] = Field(None, example="STRING", description="Kiểu dữ liệu: 'STRING', 'INTEGER', 'BOOLEAN', hoặc 'JSON'")


class UserSettingBaseResponse(BaseModel):
    setting_id: int = Field(..., description="ID của setting (integer)")
    user_id: int = Field(..., description="ID của user sở hữu setting (integer)")
    setting_key: Optional[str] = Field(None, description="Khóa của setting (string)")
    setting_value: Optional[str] = Field(None, description="Giá trị của setting (string)")
    data_type: Optional[str] = Field(None, description="Kiểu dữ liệu: 'STRING', 'INTEGER', 'BOOLEAN', hoặc 'JSON' (string)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")


class DefaultSettingCreateRequest(BaseModel):
    setting_key: str = Field(..., example="focus_duration", description="Khóa của setting (string)")
    default_value: Optional[str] = Field(None, example="25", description="Giá trị mặc định (string)")
    data_type: Optional[str] = Field(None, example="STRING", description="Kiểu dữ liệu: 'STRING', 'INTEGER', 'BOOLEAN', hoặc 'JSON' (string)")
    category: Optional[str] = Field(None, example="TIMER", description="Danh mục: 'TIMER', 'NOTIFICATION', 'APPEARANCE', hoặc 'DATA' (string)")
    description: Optional[str] = Field(None, example="Thời lượng focus session mặc định", description="Mô tả về setting (string)")
    is_configurable: Optional[int] = Field(1, example=1, description="Có thể cấu hình hay không: 0 = không, 1 = có (integer, mặc định: 1)")


class DefaultSettingUpdateRequest(BaseModel):
    setting_key: Optional[str] = Field(None, example="focus_duration", description="Khóa của setting (string)")
    default_value: Optional[str] = Field(None, example="30", description="Giá trị mặc định (string)")
    data_type: Optional[str] = Field(None, example="STRING", description="Kiểu dữ liệu: 'STRING', 'INTEGER', 'BOOLEAN', hoặc 'JSON'")
    category: Optional[str] = Field(None, example="TIMER", description="Danh mục: 'TIMER', 'NOTIFICATION', 'APPEARANCE', hoặc 'DATA'")
    description: Optional[str] = Field(None, example="Thời lượng focus session mặc định", description="Mô tả về setting (string)")
    is_configurable: Optional[int] = Field(None, example=1, description="Có thể cấu hình hay không: 0 = không, 1 = có (integer)")


class DefaultSettingBaseResponse(BaseModel):
    default_setting_id: int = Field(..., description="ID của default setting (integer)")
    setting_key: Optional[str] = Field(None, description="Khóa của setting (string)")
    default_value: Optional[str] = Field(None, description="Giá trị mặc định (string)")
    data_type: Optional[str] = Field(None, description="Kiểu dữ liệu: 'STRING', 'INTEGER', 'BOOLEAN', hoặc 'JSON' (string)")
    category: Optional[str] = Field(None, description="Danh mục: 'TIMER', 'NOTIFICATION', 'APPEARANCE', hoặc 'DATA' (string)")
    description: Optional[str] = Field(None, description="Mô tả về setting (string)")
    is_configurable: Optional[int] = Field(None, description="Có thể cấu hình hay không: 0 = không, 1 = có (integer)")
    created_at: Optional[float] = Field(None, description="Thời gian tạo (Unix timestamp - float)")
    updated_at: Optional[float] = Field(None, description="Thời gian cập nhật lần cuối (Unix timestamp - float)")

