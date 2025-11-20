from fastapi_sqlalchemy import db
from app.models.model_user_entity import UserEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from typing import Any, Dict


class UserEntityService(BaseService[UserEntity]):

    def __init__(self):
        super().__init__(UserEntity)

    def create(self, data: Dict[str, Any]) -> UserEntity:
        """
        Create a new UserEntity with duplicate email check
        """
        # Check if email already exists
        if "email" in data and data["email"]:
            existing = self.check_duplicate({"email": data["email"]})
            if existing:
                raise CustomException(
                    exception=ExceptionType.DUPLICATE_ENTRY,
                    message=f"Email {data['email']} already exists"
                )
        
        return super().create(data, duplicate_check={"email": data.get("email")} if data.get("email") else None)

