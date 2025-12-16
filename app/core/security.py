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
        print("========== FIREBASE APP ALREADY INITIALIZED ==========", flush=True)
    except ValueError:
        # Initialize Firebase Admin SDK if not already initialized
        try:
            # Firebase options with project ID
            firebase_options = {
                'projectId': settings.FIREBASE_PROJECT_ID,
            }
            
            if settings.FIREBASE_CREDENTIALS_PATH:
                # Use service account credentials file
                import os
                cred_path = os.path.abspath(settings.FIREBASE_CREDENTIALS_PATH)
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    _firebase_app = firebase_admin.initialize_app(cred, firebase_options)
                    print(f"========== FIREBASE INITIALIZED WITH CREDENTIALS FILE: {cred_path} ==========", flush=True)
                    print(f"Project ID: {settings.FIREBASE_PROJECT_ID}", flush=True)
                else:
                    print(f"========== FIREBASE CREDENTIALS FILE NOT FOUND: {cred_path} ==========", flush=True)
                    # Try to initialize with project ID only (for GCP environments)
                    _firebase_app = firebase_admin.initialize_app(options=firebase_options)
                    print("========== FIREBASE INITIALIZED WITH PROJECT ID ONLY (using ADC) ==========", flush=True)
                    print(f"Project ID: {settings.FIREBASE_PROJECT_ID}", flush=True)
            else:
                # Try to use Application Default Credentials (ADC) or environment variable
                import os
                google_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
                if google_creds and os.path.exists(google_creds):
                    cred = credentials.Certificate(google_creds)
                    _firebase_app = firebase_admin.initialize_app(cred, firebase_options)
                    print(f"========== FIREBASE INITIALIZED WITH GOOGLE_APPLICATION_CREDENTIALS: {google_creds} ==========", flush=True)
                    print(f"Project ID: {settings.FIREBASE_PROJECT_ID}", flush=True)
                else:
                    # Try to initialize with project ID only (for GCP environments)
                    _firebase_app = firebase_admin.initialize_app(options=firebase_options)
                    print("========== FIREBASE INITIALIZED WITH PROJECT ID ONLY (using ADC) ==========", flush=True)
                    print(f"Project ID: {settings.FIREBASE_PROJECT_ID}", flush=True)
        except Exception as e:
            print(f"========== FIREBASE INITIALIZATION FAILED ==========", flush=True)
            print(f"Error: {str(e)}", flush=True)
            print(f"Error type: {type(e).__name__}", flush=True)
            _firebase_app = None
else:
    print("========== FIREBASE_PROJECT_ID NOT SET ==========", flush=True)


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


def verify_firebase_token(firebase_id_token: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Verify Firebase ID Token and return decoded token claims.
    Returns (decoded_token, error_message) tuple.
    If successful, returns (decoded_token, None).
    If failed, returns (None, error_message).
    """
    if not _firebase_app:
        error_msg = "Firebase chưa được cấu hình. Vui lòng set FIREBASE_PROJECT_ID trong file .env"
        print("========== FIREBASE NOT CONFIGURED ==========", flush=True)
        print(f"FIREBASE_PROJECT_ID: {settings.FIREBASE_PROJECT_ID}", flush=True)
        return None, error_msg
    
    try:
        decoded_token = auth.verify_id_token(firebase_id_token)
        print("========== FIREBASE TOKEN VERIFIED SUCCESSFULLY ==========", flush=True)
        return decoded_token, None
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print("========== FIREBASE TOKEN VERIFICATION FAILED ==========", flush=True)
        print(f"Error: {error_msg}", flush=True)
        print(f"Error type: {error_type}", flush=True)
        
        # Check for specific error types
        if "DefaultCredentialsError" in error_type or "credentials" in error_msg.lower():
            detailed_error = "Firebase cần Service Account Credentials. Vui lòng: 1) Tải Service Account Key từ Firebase Console, 2) Đặt file vào thư mục backend, 3) Set FIREBASE_CREDENTIALS_PATH trong .env"
        elif "invalid" in error_msg.lower() or "expired" in error_msg.lower():
            detailed_error = "Firebase ID Token không hợp lệ hoặc đã hết hạn"
        else:
            detailed_error = f"Lỗi xác thực Firebase: {error_msg}"
        
        return None, detailed_error


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
        print("========== JWTBearer Called ==========", flush=True)
        print(f"Request path: {request.url.path}", flush=True)
        auth_header = request.headers.get('authorization')
        print(f"Authorization header: {'Found' if auth_header else 'NOT FOUND - Please include Authorization: Bearer <token> header'}", flush=True)
        
        if not auth_header:
            print("ERROR: Missing Authorization header. Please include 'Authorization: Bearer <token>' in request headers.", flush=True)
            raise CustomException(
                exception=ExceptionType.UNAUTHORIZED,
                message="Missing Authorization header. Please include 'Authorization: Bearer <token>' in request headers."
            )
        
        try:
            credentials: HTTPAuthorizationCredentials = await super(
                JWTBearer, self
            ).__call__(request)
            if credentials is None:
                print("JWTBearer: credentials is None", flush=True)
                raise CustomException(
                    exception=ExceptionType.UNAUTHORIZED,
                    message="Invalid Authorization header format. Expected: 'Authorization: Bearer <token>'"
                )
            if not credentials.credentials:
                print("JWTBearer: credentials.credentials is empty", flush=True)
                raise CustomException(
                    exception=ExceptionType.UNAUTHORIZED,
                    message="Token is empty. Please provide a valid JWT token."
                )
            if not credentials.scheme == "Bearer":
                print(f"JWTBearer: Invalid scheme: {credentials.scheme}. Expected 'Bearer'", flush=True)
                raise CustomException(
                    exception=ExceptionType.UNAUTHORIZED,
                    message=f"Invalid authorization scheme: {credentials.scheme}. Expected 'Bearer'."
                )
            if not self.verify_jwt(credentials.credentials):
                print("JWTBearer: JWT verification failed - token invalid or expired", flush=True)
                raise CustomException(
                    exception=ExceptionType.UNAUTHORIZED,
                    message="Invalid or expired token. Please login again to get a new token."
                )
            print("JWTBearer: Token verified successfully", flush=True)
            return credentials.credentials
        except CustomException as e:
            print(f"JWTBearer: CustomException raised: {e.http_code} - {e.message}", flush=True)
            raise
        except Exception as e:
            print(f"JWTBearer: Unexpected exception: {type(e).__name__}: {str(e)}", flush=True)
            if "Not authenticated" in str(e) or "403" in str(e):
                raise CustomException(
                    exception=ExceptionType.UNAUTHORIZED,
                    message="Authentication required. Please include 'Authorization: Bearer <token>' header."
                )
            raise CustomException(exception=ExceptionType.UNAUTHORIZED)

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
