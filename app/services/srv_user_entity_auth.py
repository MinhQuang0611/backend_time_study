from fastapi_sqlalchemy import db
from sqlalchemy import or_
from app.models.model_user_entity import UserEntity
from app.core.security import (
    verify_password, 
    create_access_token, 
    get_password_hash,
    verify_firebase_token,
    create_refresh_token,
    verify_refresh_token
)
from app.schemas.sche_user_entity_auth import (
    UserEntityRegisterRequest, 
    UserEntityLoginRequest, 
    UserEntityTokenResponse,
    FirebaseLoginRequest,
    RefreshTokenRequest
)
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
        print(f"========== LOGIN ATTEMPT ==========", flush=True)
        print(f"Email: {email}", flush=True)
        
        if not email or not password:
            print("Missing email or password", flush=True)
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Email và mật khẩu không được để trống"
            )
        
        user = db.session.query(UserEntity).filter(UserEntity.email == email).first()
        if not user:
            print(f"User not found: {email}", flush=True)
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Tài khoản không tồn tại"
            )
        
        print(f"User found: {user.user_id}, has_password: {bool(user.hashed_password)}", flush=True)
        
        if not user.hashed_password:
            print("User has no password", flush=True)
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Tài khoản này chưa được thiết lập mật khẩu. Vui lòng đăng nhập bằng phương thức khác hoặc đặt lại mật khẩu."
            )
        
        if not verify_password(password, user.hashed_password):
            print("Password verification failed", flush=True)
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Email hoặc mật khẩu không đúng"
            )
        
        print("Password verified successfully", flush=True)

        user.last_login = time_utils.timestamp_now()
        db.session.commit()
        
        access_token, expire = create_access_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.user_id),
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
    def login_firebase(data: FirebaseLoginRequest) -> UserEntityTokenResponse:
        """
        Login with Firebase ID Token.
        Verify Firebase token, find or create user, then return access_token and refresh_token.
        """
        print("========== FIREBASE LOGIN API CALLED ==========", flush=True)
        firebase_id_token = data.firebase_id_token
        if not firebase_id_token:
            print("========== FIREBASE ID TOKEN MISSING ==========", flush=True)
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Firebase ID Token không được để trống"
            )
        
        print(f"========== VERIFYING FIREBASE TOKEN ==========", flush=True)
        print(f"Token length: {len(firebase_id_token) if firebase_id_token else 0}", flush=True)
        
        # Verify Firebase ID Token
        decoded_token, error_message = verify_firebase_token(firebase_id_token)
        if not decoded_token:
            print("========== FIREBASE TOKEN VERIFICATION FAILED ==========", flush=True)
            # Check if Firebase is configured
            from app.core.config import settings
            if not settings.FIREBASE_PROJECT_ID:
                raise CustomException(
                    exception=ExceptionType.INTERNAL_SERVER_ERROR,
                    message="Firebase chưa được cấu hình. Vui lòng set FIREBASE_PROJECT_ID trong file .env"
                )
            # Use detailed error message from verify_firebase_token
            if "credentials" in error_message.lower() or "Service Account" in error_message:
                raise CustomException(
                    exception=ExceptionType.INTERNAL_SERVER_ERROR,
                    message=error_message
                )
            else:
                raise CustomException(
                    exception=ExceptionType.UNAUTHORIZED,
                    message=error_message or "Firebase ID Token không hợp lệ hoặc đã hết hạn"
                )
        
        # Extract user info from Firebase token
        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")
        # Check if login via Facebook
        firebase_provider = decoded_token.get("firebase", {}).get("sign_in_provider")
        is_facebook = firebase_provider == "facebook.com" if firebase_provider else False
        
        if not firebase_uid:
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Firebase token không hợp lệ"
            )
        
        # Find or create user
        # First, try to find by email (if email exists)
        user = None
        if email:
            user = db.session.query(UserEntity).filter(UserEntity.email == email).first()
        
        # If not found, create new user
        if not user:
            # Generate email if not provided (for Facebook login without email)
            if not email:
                email = f"fb_{firebase_uid}@facebook.temp"  # Temporary email, user can update later
            
            user = UserEntity(
                email=email,
                display_name=name,
                profile_picture_url=picture,
                hashed_password=None,  # No password for Firebase users
                is_anonymous=0,  # Firebase users are not anonymous
                last_login=time_utils.timestamp_now(),
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            
            # If login via Facebook, create ExternalAccount record
            if is_facebook:
                from app.models.model_external_account import ExternalAccount
                import time as time_module
                # Get Facebook ID from token (if available)
                facebook_id = decoded_token.get("providerData", [{}])[0].get("uid") if decoded_token.get("providerData") else firebase_uid
                
                fb_account = ExternalAccount(
                    user_id=user.user_id,
                    provider="facebook",
                    provider_user_id=facebook_id or firebase_uid,
                    name=name,
                    avatar_url=picture,
                    created_at=time_module.time(),
                )
                db.session.add(fb_account)
                db.session.commit()
        else:
            # Update last login
            user.last_login = time_utils.timestamp_now()
            # Update user info if available
            if name and not user.display_name:
                user.display_name = name
            if picture and not user.profile_picture_url:
                user.profile_picture_url = picture
            db.session.commit()
            
            # If login via Facebook and not linked yet, create ExternalAccount
            if is_facebook:
                from app.models.model_external_account import ExternalAccount
                import time as time_module
                from sqlalchemy import select
                
                # Check if already linked
                existing_fb = db.session.execute(
                    select(ExternalAccount).where(
                        ExternalAccount.user_id == user.user_id,
                        ExternalAccount.provider == "facebook"
                    )
                ).scalar_one_or_none()
                
                if not existing_fb:
                    facebook_id = decoded_token.get("providerData", [{}])[0].get("uid") if decoded_token.get("providerData") else firebase_uid
                    fb_account = ExternalAccount(
                        user_id=user.user_id,
                        provider="facebook",
                        provider_user_id=facebook_id or firebase_uid,
                        name=name,
                        avatar_url=picture,
                        created_at=time_module.time(),
                    )
                    db.session.add(fb_account)
                    db.session.commit()
        
        # Create access token
        access_token, access_expire = create_access_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.user_id),
                typ="Bearer",
                email=user.email if user.email else None,
            )
        )
        
        # Create refresh token
        refresh_token, refresh_expire = create_refresh_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.user_id),
                typ="refresh",
                email=user.email if user.email else None,
            )
        )
        
        user_data = UserEntityBaseResponse.model_validate(user, from_attributes=True)
        
        res_token = UserEntityTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_expire,
            refresh_expires_in=refresh_expire,
            token_type="Bearer",
            user=user_data.model_dump(exclude={"hashed_password"} if hasattr(user, "hashed_password") else set())
        )
        return res_token

    @staticmethod
    def refresh_token(data: RefreshTokenRequest) -> UserEntityTokenResponse:
        """
        Refresh access token using refresh token.
        """
        refresh_token = data.refresh_token
        if not refresh_token:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Verify refresh token
        decoded_token = verify_refresh_token(refresh_token)
        if not decoded_token:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Get user ID from refresh token
        user_id = decoded_token.get("sub")
        if not user_id:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Find user
        user = db.session.query(UserEntity).filter(UserEntity.user_id == int(user_id)).first()
        if not user:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Create new access token
        access_token, access_expire = create_access_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.user_id),
                typ="Bearer",
                email=user.email if user.email else None,
            )
        )
        
        # Optionally create new refresh token (rotate refresh token)
        new_refresh_token, refresh_expire = create_refresh_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.user_id),
                typ="refresh",
                email=user.email if user.email else None,
            )
        )
        
        user_data = UserEntityBaseResponse.model_validate(user, from_attributes=True)
        
        res_token = UserEntityTokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=access_expire,
            refresh_expires_in=refresh_expire,
            token_type="Bearer",
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

