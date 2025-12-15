from typing import Tuple, Any, Optional, Dict

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
import firebase_admin
from firebase_admin import auth, credentials

from app.core.config import settings
from app.utils.exception_handler import CustomException, ExceptionType
from app.utils import time_utils
from app.schemas.sche_auth import TokenRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

# Initialize Firebase Admin SDK
_firebase_app = None
if settings.FIREBASE_PROJECT_ID:
    try:
        _firebase_app = firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase Admin SDK if not already initialized
        # You can also use service account credentials file if needed
        # cred = credentials.Certificate("path/to/serviceAccountKey.json")
        # firebase_admin.initialize_app(cred)
        firebase_admin.initialize_app()


def create_access_token(
    payload: TokenRequest, expires_seconds: int = None
) -> Tuple[str, float]:
    if expires_seconds:
        expire = time_utils.timestamp_after_now(seconds=expires_seconds)
    else:
        expire = time_utils.timestamp_after_now(
            seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
        )
    encoded_jwt = jwt.encode(
        payload.model_dump(), settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt, expire


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_firebase_token(firebase_id_token: str) -> Optional[Dict[str, Any]]:
    """
    Verify Firebase ID Token and return decoded token claims.
    Returns None if token is invalid or Firebase is not configured.
    """
    if not _firebase_app:
        return None
    
    try:
        decoded_token = auth.verify_id_token(firebase_id_token)
        return decoded_token
    except Exception as e:
        return None


def create_refresh_token(
    payload: TokenRequest, expires_seconds: int = None
) -> Tuple[str, float]:
    """
    Create a refresh token with longer expiration time.
    """
    if expires_seconds:
        expire = time_utils.timestamp_after_now(seconds=expires_seconds)
    else:
        expire = time_utils.timestamp_after_now(
            seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS
        )
    
    # Create payload dict and override exp and typ for refresh token
    payload_dict = payload.model_dump()
    payload_dict["exp"] = expire
    payload_dict["typ"] = "refresh"
    
    encoded_jwt = jwt.encode(
        payload_dict, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt, expire


def verify_refresh_token(refresh_token: str) -> Optional[Dict[str, Any]]:
    """
    Verify refresh token and return decoded payload.
    Returns None if token is invalid or expired.
    """
    try:
        decoded_token = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=ALGORITHM)
        # Check if it's a refresh token
        if decoded_token.get("typ") != "refresh":
            return None
        # Check expiration
        if decoded_token.get("exp", 0) < time_utils.timestamp_now():
            return None
        return decoded_token
    except Exception as e:
        return None


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
        if decoded_token["exp"] >= time_utils.timestamp_now():
            return decoded_token
        return None
    except Exception as e:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials is None:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        if not credentials.credentials:
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        if not credentials.scheme == "Bearer":
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        if not self.verify_jwt(credentials.credentials):
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)
        return credentials.credentials

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
