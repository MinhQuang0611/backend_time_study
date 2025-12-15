from fastapi_sqlalchemy import db
from sqlalchemy import or_
from app.models import User
from app.core.security import (
    verify_password, 
    create_access_token, 
    get_password_hash,
    verify_firebase_token,
    create_refresh_token,
    verify_refresh_token
)
from app.schemas.sche_auth import (
    RegisterRequest, 
    LoginRequest, 
    FirebaseLoginRequest,
    RefreshTokenRequest
)
from app.schemas.sche_user import UserBaseResponse
from app.schemas.sche_auth import TokenResponse, TokenRequest
from app.utils.exception_handler import CustomException, ExceptionType
from app.core.config import keycloak_openid, settings
from app.utils.enums import UserRole
from app.utils import time_utils


class AuthService(object):
    __instance = None

    @staticmethod
    def login(data: LoginRequest) -> TokenResponse:
        username = data.username
        password = data.password
        if not username or not password:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        user = (
            db.session.query(User)
            .filter(or_(User.username == username, User.email == username))
            .first()
        )
        if not user:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        if not verify_password(password, user.hashed_password):
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        elif not user.is_active:
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
        res_token = TokenResponse(
            access_token=access_token, expires_in=expire, refresh_expires_in=expire
        )
        return res_token

    @staticmethod
    def login_keycloak(data: LoginRequest) -> TokenResponse:
        try:
            username = data.username
            password = data.password
            if not username or not password:
                raise CustomException(exception=ExceptionType.UNAUTHORIZED)
            token = keycloak_openid.token(username, password)
            res_token = TokenResponse(**token)
            return res_token
        except Exception:
            return None

    @staticmethod
    def register(data: RegisterRequest) -> UserBaseResponse:
        exist_user = db.session.query(User).filter(User.email == data.email).first()
        if exist_user:
            raise CustomException(exception=ExceptionType.CONFLICT)
        register_user = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=get_password_hash(data.password),
            roles=[UserRole.USER.name],
            is_active=True,
            last_login=time_utils.timestamp_now(),
        )
        db.session.add(register_user)
        db.session.commit()
        return UserBaseResponse.model_validate(register_user, from_attributes=True)

    @staticmethod
    def login_firebase(data: FirebaseLoginRequest) -> TokenResponse:
        """
        Login with Firebase ID Token.
        Verify Firebase token, find or create user, then return access_token and refresh_token.
        """
        firebase_id_token = data.firebase_id_token
        if not firebase_id_token:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Verify Firebase ID Token
        decoded_token = verify_firebase_token(firebase_id_token)
        if not decoded_token:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Extract user info from Firebase token
        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")
        
        if not firebase_uid:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Find or create user
        # First, try to find by sso_sub (Firebase UID)
        user = db.session.query(User).filter(User.sso_sub == firebase_uid).first()
        
        # If not found, try to find by email
        if not user and email:
            user = db.session.query(User).filter(User.email == email).first()
            # If found by email, update sso_sub to link Firebase account
            if user:
                user.sso_sub = firebase_uid
        
        # If still not found, create new user
        if not user:
            # Generate username from email or use Firebase UID
            username = email.split("@")[0] if email else f"user_{firebase_uid[:8]}"
            # Ensure username is unique
            base_username = username
            counter = 1
            while db.session.query(User).filter(User.username == username).first():
                username = f"{base_username}_{counter}"
                counter += 1
            
            user = User(
                sso_sub=firebase_uid,
                username=username,
                email=email,
                full_name=name,
                is_active=True,
                roles=[UserRole.USER.name],
                last_login=time_utils.timestamp_now(),
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
        else:
            # Update last login
            user.last_login = time_utils.timestamp_now()
            # Update user info if available
            if name and not user.full_name:
                user.full_name = name
            db.session.commit()
        
        # Create access token
        access_token, access_expire = create_access_token(
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
        
        # Create refresh token
        refresh_token, refresh_expire = create_refresh_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.id),
                typ="refresh",
                email=user.email if user.email else None,
            )
        )
        
        res_token = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_expire,
            refresh_expires_in=refresh_expire,
            token_type="Bearer"
        )
        return res_token

    @staticmethod
    def refresh_token(data: RefreshTokenRequest) -> TokenResponse:
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
        user = db.session.query(User).get(user_id)
        if not user or not user.is_active:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        
        # Create new access token
        access_token, access_expire = create_access_token(
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
        
        # Optionally create new refresh token (rotate refresh token)
        new_refresh_token, refresh_expire = create_refresh_token(
            TokenRequest(
                exp=time_utils.timestamp_after_now(
                    seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
                ),
                auth_time=time_utils.timestamp_now(),
                sub=str(user.id),
                typ="refresh",
                email=user.email if user.email else None,
            )
        )
        
        res_token = TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=access_expire,
            refresh_expires_in=refresh_expire,
            token_type="Bearer"
        )
        return res_token
