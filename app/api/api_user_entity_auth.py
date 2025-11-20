from typing import Any

from fastapi import APIRouter, Depends
from app.schemas.sche_response import DataResponse
from app.services.srv_user_entity_auth import UserEntityAuthService
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_user_entity_auth import (
    UserEntityLoginRequest,
    UserEntityRegisterRequest,
    UserEntityTokenResponse,
)
from app.schemas.sche_user_entity import UserEntityBaseResponse

router = APIRouter(prefix=f"/auth/user-entity")


@router.post("/login", response_model=DataResponse[UserEntityTokenResponse])
def login(form_data: UserEntityLoginRequest, auth_service: UserEntityAuthService = Depends()):
    try:
        token = UserEntityAuthService.login(data=form_data)
        return DataResponse(http_code=200, data=token)
    except Exception as e:
        print(e, flush=True)
        raise CustomException(exception=e)


@router.post("/register", response_model=DataResponse[UserEntityBaseResponse])
def register(data: UserEntityRegisterRequest, auth_service: UserEntityAuthService = Depends()) -> Any:
    try:
        register_user = UserEntityAuthService.register(data)
        return DataResponse(http_code=201, data=register_user)
    except Exception as e:
        raise CustomException(exception=e)

