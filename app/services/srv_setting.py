from fastapi_sqlalchemy import db
from app.models.model_setting import UserSettingEntity, DefaultSettingEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from typing import Any, Dict


class UserSettingService(BaseService[UserSettingEntity]):

    def __init__(self):
        super().__init__(UserSettingEntity)

    def create(self, data: Dict[str, Any]) -> UserSettingEntity:
        """
        Create a new UserSettingEntity with duplicate check for user_id + setting_key
        """
        # Check unique constraint: user_id + setting_key
        if "user_id" in data and "setting_key" in data:
            existing = self.check_duplicate({
                "user_id": data["user_id"],
                "setting_key": data["setting_key"]
            })
            if existing:
                raise CustomException(
                    exception=ExceptionType.DUPLICATE_ENTRY,
                    message=f"Setting {data['setting_key']} for user {data['user_id']} already exists"
                )
        
        return super().create(data)


class DefaultSettingService(BaseService[DefaultSettingEntity]):

    def __init__(self):
        super().__init__(DefaultSettingEntity)

    def create(self, data: Dict[str, Any]) -> DefaultSettingEntity:
        """
        Create a new DefaultSettingEntity with duplicate check for setting_key
        """
        # Check unique constraint: setting_key
        if "setting_key" in data:
            existing = self.check_duplicate({"setting_key": data["setting_key"]})
            if existing:
                raise CustomException(
                    exception=ExceptionType.DUPLICATE_ENTRY,
                    message=f"Default setting {data['setting_key']} already exists"
                )
        
        return super().create(data)

