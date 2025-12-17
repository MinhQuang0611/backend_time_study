from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.schemas.sche_response import DataResponse
from app.schemas.sche_user_entity import UserEntityBaseResponse
from app.schemas.sche_external_account import (
    FacebookLinkRequest, 
    FacebookLinkResponse,
    FacebookFriendsRequest,
    FacebookFriendsResponse
)
from app.services.srv_user_entity_auth import UserEntityAuthService
from app.schemas.sche_user_entity_auth import (
    UserEntityLoginRequest,
    UserEntityRegisterRequest,
    UserEntityTokenResponse,
    FirebaseLoginRequest,
    RefreshTokenRequest,
)
from app.services.srv_external_account import link_facebook_account, sync_facebook_friends, migrate_external_accounts_to_facebook_ids
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
    """
    Link hoặc update Facebook account với Facebook ID thực sự.
    Nếu đã có external_account, sẽ update provider_user_id với Facebook ID mới.
    """
    link_facebook_account(
        db=db,
        user_id=current_user.user_id,
        facebook_id=data.facebook_id,
        name=data.name,
        picture=data.picture,
    )

    return {"message": "Facebook linked/updated successfully"}


@router.post("/sync/facebook-friends", response_model=DataResponse[FacebookFriendsResponse])
def sync_facebook_friends_api(
    data: FacebookFriendsRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    db: Session = Depends(get_db),
):
    """
    Đồng bộ danh sách bạn bè Facebook từ Facebook Graph API.
    Gọi Facebook Graph API /me/friends và lưu vào database.
    """
    print("========== SYNC FACEBOOK FRIENDS API CALLED ==========", flush=True)
    print(f"Current user ID: {current_user.user_id if current_user else 'None'}", flush=True)
    print(f"Access token received: {bool(data.access_token)}", flush=True)
    try:
        result = sync_facebook_friends(
            db=db,
            user_id=current_user.user_id,
            access_token=data.access_token,
        )
        print("========== SYNC FACEBOOK FRIENDS SUCCESS ==========", flush=True)
        return DataResponse(http_code=200, data=result)
    except Exception as e:
        print(f"========== ERROR SYNCING FACEBOOK FRIENDS ==========", flush=True)
        print(f"Error type: {type(e).__name__}", flush=True)
        print(f"Error message: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        print("====================================================", flush=True)
        raise CustomException(exception=e)


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


@router.post("/migrate/facebook-ids", response_model=DataResponse[dict])
def migrate_facebook_ids(
    db: Session = Depends(get_db),
):
    """
    Migration API: Tự động update tất cả external_accounts từ Firebase UID sang Facebook ID thực sự.
    
    Chạy một lần để fix tất cả external_accounts hiện tại.
    Logic:
    1. Tìm tất cả external_accounts có provider='facebook' và provider_user_id là Firebase UID
    2. Extract Facebook ID từ profile_picture_url của user (dạng https://graph.facebook.com/{facebook_id}/picture)
    3. Update external_account với Facebook ID đó
    
    LƯU Ý: API này chỉ chạy một lần, sau đó có thể disable hoặc xóa.
    """
    try:
        result = migrate_external_accounts_to_facebook_ids(db=db)
        return DataResponse(http_code=200, data=result)
    except Exception as e:
        print(f"Migration error: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        raise CustomException(exception=e)
