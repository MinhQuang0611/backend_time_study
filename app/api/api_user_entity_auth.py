from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.schemas.sche_response import DataResponse
from app.schemas.sche_user_entity import UserEntityBaseResponse
from app.schemas.sche_external_account import FacebookLinkRequest, FacebookLinkResponse
from app.services.srv_user_entity_auth import UserEntityAuthService
from app.schemas.sche_user_entity_auth import (
    UserEntityLoginRequest,
    UserEntityRegisterRequest,
    UserEntityTokenResponse,
    FirebaseLoginRequest,
    RefreshTokenRequest,
)
from app.services.srv_external_account import link_facebook_account
from app.utils.exception_handler import CustomException, ExceptionType
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/auth/user-entity")


@router.post("/login", response_model=DataResponse[UserEntityTokenResponse])
def login(form_data: UserEntityLoginRequest, auth_service: UserEntityAuthService = Depends()):
    print(f"========== LOGIN API CALLED ==========", flush=True)
    print(f"Request data: {form_data.model_dump()}", flush=True)
    try:
        token = UserEntityAuthService.login(data=form_data)
        print(f"Login successful, returning token", flush=True)
        return DataResponse(http_code=200, data=token)
    except CustomException as e:
        print(f"CustomException raised: {e.http_code} - {e.message}", flush=True)
        raise
    except Exception as e:
        print(f"Unexpected exception: {type(e).__name__}: {str(e)}", flush=True)
        raise CustomException(exception=ExceptionType.INTERNAL_SERVER_ERROR)


@router.post("/register", response_model=DataResponse[UserEntityBaseResponse])
def register(data: UserEntityRegisterRequest, auth_service: UserEntityAuthService = Depends()) -> Any:
    try:
        register_user = UserEntityAuthService.register(data)
        return DataResponse(http_code=201, data=register_user)
    except Exception as e:
        raise CustomException(exception=e)


@router.post("/link/facebook", response_model=FacebookLinkResponse)
def link_facebook(
    data: FacebookLinkRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    db: Session = Depends(get_db),
):
    link_facebook_account(
        db=db,
        user_id=current_user.user_id,
        facebook_id=data.facebook_id,
        name=data.name,
        picture=data.picture,
    )

    return {"message": "Facebook linked successfully"}


@router.post("/login-firebase", response_model=DataResponse[UserEntityTokenResponse])
def login_firebase(data: FirebaseLoginRequest, auth_service: UserEntityAuthService = Depends()):
    """
    Login with Firebase ID Token.
    Returns access_token and refresh_token.
    """
    try:
        token = UserEntityAuthService.login_firebase(data=data)
        return DataResponse(http_code=200, data=token)
    except Exception as e:
        print(e, flush=True)
        raise CustomException(exception=e)


@router.post("/refresh-token", response_model=DataResponse[UserEntityTokenResponse])
def refresh_token(data: RefreshTokenRequest, auth_service: UserEntityAuthService = Depends()):
    """
    Refresh access token using refresh token.
    Returns new access_token and refresh_token.
    """
    try:
        token = UserEntityAuthService.refresh_token(data=data)
        return DataResponse(http_code=200, data=token)
    except Exception as e:
        print(e, flush=True)
        raise CustomException(exception=e)
