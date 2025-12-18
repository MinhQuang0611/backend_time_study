from typing import Any
from fastapi import APIRouter, Depends, status, Query
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_user_coin import (
    UserCoinCreateRequest,
    UserCoinUpdateRequest,
    UserCoinBaseResponse,
)
from app.services.srv_user_coin import UserCoinService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix="/user-coin")

user_coin_service: UserCoinService = UserCoinService()


@router.get(
    "/me",
    response_model=DataResponse[UserCoinBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_coin(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy coin của user hiện tại (tự động tạo nếu chưa có)
    Trả về đầy đủ thông tin: coin_id, user_id, coin, created_at, updated_at
    """
    try:
        coin = user_coin_service.get_or_create_coin(current_user.user_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=coin)
    except Exception as e:
        raise CustomException(exception=e)


@router.post(
    "",
    response_model=DataResponse[UserCoinBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_coin(
    coin_data: UserCoinCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo coin record mới cho user (nếu chưa có)
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_user_coin import UserCoinEntity
        
        existing = db.session.query(UserCoinEntity).filter(
            UserCoinEntity.user_id == current_user.user_id
        ).first()
        
        if existing:
            raise CustomException(
                exception=ExceptionType.BAD_REQUEST,
                message="Coin record đã tồn tại cho user này"
            )
        
        coin_dict = coin_data.model_dump()
        coin_dict["user_id"] = current_user.user_id
        new_coin = user_coin_service.create(data=coin_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_coin)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/coin",
    response_model=DataResponse[UserCoinBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_coin(
    coin_data: UserCoinUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Cập nhật số coin của user hiện tại
    """
    try:
        if coin_data.coin is None:
            raise CustomException(
                exception=ExceptionType.BAD_REQUEST,
                message="coin là bắt buộc"
            )
        
        updated_coin = user_coin_service.set_coin(
            user_id=current_user.user_id,
            coin_amount=coin_data.coin
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_coin)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/coin/add",
    response_model=DataResponse[UserCoinBaseResponse],
    status_code=status.HTTP_200_OK,
)
def add_coin(
    amount: int = Query(..., ge=1, description="Số coin cần thêm (>= 1)"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Thêm coin cho user
    """
    try:
        updated_coin = user_coin_service.add_coin(
            user_id=current_user.user_id,
            amount=amount
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_coin)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/coin/subtract",
    response_model=DataResponse[UserCoinBaseResponse],
    status_code=status.HTTP_200_OK,
)
def subtract_coin(
    amount: int = Query(..., ge=1, description="Số coin cần trừ (>= 1)"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Trừ coin của user (kiểm tra đủ coin trước khi trừ)
    """
    try:
        updated_coin = user_coin_service.subtract_coin(
            user_id=current_user.user_id,
            amount=amount
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_coin)
    except Exception as e:
        raise CustomException(exception=e)

