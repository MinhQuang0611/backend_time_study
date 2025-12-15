from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_setting import (
    UserSettingCreateRequest,
    UserSettingUpdateRequest,
    UserSettingBaseResponse,
    DefaultSettingCreateRequest,
    DefaultSettingUpdateRequest,
    DefaultSettingBaseResponse,
)
from app.services.srv_setting import UserSettingService, DefaultSettingService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/settings")

user_setting_service: UserSettingService = UserSettingService()
default_setting_service: DefaultSettingService = DefaultSettingService()


# User Setting endpoints
@router.get(
    "/user/all",
    response_model=DataResponse[List[UserSettingBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_user_settings(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired())
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_setting import UserSettingEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        query = db.session.query(UserSettingEntity).filter(UserSettingEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=UserSettingEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/user",
    response_model=DataResponse[List[UserSettingBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_user_settings_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_setting import UserSettingEntity
        from app.utils.paging import paginate
        query = db.session.query(UserSettingEntity).filter(UserSettingEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=UserSettingEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/user",
    response_model=DataResponse[UserSettingBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user_setting(
    setting_data: UserSettingCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        setting_dict = setting_data.model_dump()
        setting_dict["user_id"] = current_user.user_id
        new_setting = user_setting_service.create(data=setting_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/user/{setting_id}",
    response_model=DataResponse[UserSettingBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_user_setting_by_id(
    setting_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        setting = user_setting_service.get_by_id(setting_id)
        if setting.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/user/{setting_id}",
    response_model=DataResponse[UserSettingBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_user_setting_by_id(
    setting_id: int,
    setting_data: UserSettingUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        setting = user_setting_service.get_by_id(setting_id)
        if setting.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_setting = user_setting_service.update_by_id(setting_id, data=setting_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/user/{setting_id}",
    response_model=DataResponse[UserSettingBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_user_setting_by_id(
    setting_id: int,
    setting_data: UserSettingUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        setting = user_setting_service.get_by_id(setting_id)
        if setting.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_setting = user_setting_service.partial_update_by_id(setting_id, data=setting_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/user/{setting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_setting_by_id(
    setting_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        setting = user_setting_service.get_by_id(setting_id)
        if setting.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        user_setting_service.delete_by_id(setting_id)
    except Exception as e:
        raise CustomException(exception=e)


# Default Setting endpoints
@router.get(
    "/default/all",
    response_model=DataResponse[List[DefaultSettingBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_default_settings() -> Any:
    try:
        data, metadata = default_setting_service.get_all()
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/default",
    response_model=DataResponse[List[DefaultSettingBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_default_settings_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
) -> Any:
    try:
        data, metadata = default_setting_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/default",
    response_model=DataResponse[DefaultSettingBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_default_setting(setting_data: DefaultSettingCreateRequest) -> Any:
    try:
        new_setting = default_setting_service.create(data=setting_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/default/{default_setting_id}",
    response_model=DataResponse[DefaultSettingBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_default_setting_by_id(default_setting_id: int) -> Any:
    try:
        setting = default_setting_service.get_by_id(default_setting_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/default/{default_setting_id}",
    response_model=DataResponse[DefaultSettingBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_default_setting_by_id(default_setting_id: int, setting_data: DefaultSettingUpdateRequest) -> Any:
    try:
        updated_setting = default_setting_service.update_by_id(default_setting_id, data=setting_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/default/{default_setting_id}",
    response_model=DataResponse[DefaultSettingBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_default_setting_by_id(default_setting_id: int, setting_data: DefaultSettingUpdateRequest) -> Any:
    try:
        updated_setting = default_setting_service.partial_update_by_id(default_setting_id, data=setting_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_setting)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/default/{default_setting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_default_setting_by_id(default_setting_id: int) -> None:
    try:
        default_setting_service.delete_by_id(default_setting_id)
    except Exception as e:
        raise CustomException(exception=e)

