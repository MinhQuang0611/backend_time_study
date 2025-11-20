from fastapi_sqlalchemy import db
from sqlalchemy import or_
from app.models.model_user_entity import UserEntity
from app.core.security import verify_password, create_access_token, get_password_hash
from app.schemas.sche_user_entity_auth import UserEntityRegisterRequest, UserEntityLoginRequest, UserEntityTokenResponse
from app.schemas.sche_user_entity import UserEntityBaseResponse
from app.schemas.sche_auth import TokenRequest
from app.utils.exception_handler import CustomException, ExceptionType
from app.utils import time_utils
from app.core.config import settings
from typing import Dict, Any


class UserEntityAuthService(object):
    __instance = None

    @staticmethod
    def login(data: UserEntityLoginRequest) -> UserEntityTokenResponse:
        email = data.email
        password = data.password
        if not email or not password:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        user = db.session.query(UserEntity).filter(UserEntity.email == email).first()
        if not user:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        if not user.hashed_password:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        if not verify_password(password, user.hashed_password):
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)

        user.last_login = time_utils.timestamp_now()
        db.session.commit()
        
        access_token, expire = create_access_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.id),
                typ="Bearer",
                email=user.email if user.email else None,
            )
        )
        
        user_data = UserEntityBaseResponse.model_validate(user, from_attributes=True)
        
        res_token = UserEntityTokenResponse(
            access_token=access_token,
            expires_in=expire,
            refresh_expires_in=expire,
            user=user_data.model_dump(exclude={"hashed_password"} if hasattr(user, "hashed_password") else set())
        )
        return res_token

    @staticmethod
    def register(data: UserEntityRegisterRequest) -> UserEntityBaseResponse:
        exist_user = db.session.query(UserEntity).filter(UserEntity.email == data.email).first()
        if exist_user:
            raise CustomException(
                exception=ExceptionType.DUPLICATE_ENTRY,
                message=f"Email {data.email} already exists"
            )
        
        register_user = UserEntity(
            email=data.email,
            display_name=data.display_name,
            profile_picture_url=data.profile_picture_url,
            hashed_password=get_password_hash(data.password),
            is_anonymous=0,  # Registered user is not anonymous
            last_login=time_utils.timestamp_now(),
        )
        db.session.add(register_user)
        db.session.commit()
        db.session.refresh(register_user)
        
        return UserEntityBaseResponse.model_validate(register_user, from_attributes=True)

