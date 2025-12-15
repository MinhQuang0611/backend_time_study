from fastapi_sqlalchemy import db
from app.models.model_user_entity import UserEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from app.core.security import decode_jwt
from app.schemas.sche_auth import TokenRequest
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

    @staticmethod
    def get_me(access_token: str) -> UserEntity:
        """
        Get current UserEntity from JWT access token.
        """
        try:
            payload = decode_jwt(access_token)
            if not payload:
                raise CustomException(exception=ExceptionType.UNAUTHORIZED)
            
            token_data = TokenRequest(**payload)
            user_id = int(token_data.sub)
            
            user = db.session.query(UserEntity).filter(UserEntity.user_id == user_id).first()
            if not user:
                raise CustomException(exception=ExceptionType.UNAUTHORIZED)
            
            return user
        except Exception as e:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)

