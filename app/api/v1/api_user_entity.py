from typing import Any, List

from fastapi import APIRouter, Depends, Path, status

from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_user_entity import (
    UserEntityCreateRequest,
    UserEntityUpdateRequest,
    UserEntityBaseResponse,
)
from app.services.srv_user_entity import UserEntityService
from app.utils.logging_utils import execute_with_logging
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity
from app.utils.exception_handler import CustomException, ExceptionType

router = APIRouter(prefix=f"/user-entities")


def get_user_entity_service() -> UserEntityService:
    return UserEntityService()


@router.get(
    "/all",
    response_model=DataResponse[List[UserEntityBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[List[UserEntityBaseResponse]]:
        # Only return current user's data
        from fastapi_sqlalchemy import db
        from app.models.model_user_entity import UserEntity as UserEntityModel
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        query = db.session.query(UserEntityModel).filter(
            UserEntityModel.user_id == current_user.user_id
        )
        data, metadata = paginate(
            model=UserEntityModel,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)

    return execute_with_logging("UserEntityService.get_all", action)


@router.get(
    "",
    response_model=DataResponse[List[UserEntityBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[List[UserEntityBaseResponse]]:
        # Only return current user's data
        from fastapi_sqlalchemy import db
        from app.models.model_user_entity import UserEntity as UserEntityModel
        from app.utils.paging import paginate
        query = db.session.query(UserEntityModel).filter(
            UserEntityModel.user_id == current_user.user_id
        )
        data, metadata = paginate(
            model=UserEntityModel,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)

    return execute_with_logging("UserEntityService.get_by_filter", action)


@router.post(
    "",
    response_model=DataResponse[UserEntityBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(
    user_entity_data: UserEntityCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
        # Note: This endpoint might not be needed as users are created via registration
        # But if needed, user_id should come from JWT token
        user_dict = user_entity_data.model_dump(exclude_none=True)
        user_dict["user_id"] = current_user.user_id
        new_user_entity = user_entity_service.create(data=user_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_user_entity)

    return execute_with_logging("UserEntityService.create", action)


@router.get(
    "/{user_id}",
    response_model=DataResponse[UserEntityBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    user_id: int = Path(..., gt=0),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
        # Verify user can only access their own data
        if user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        user_entity = user_entity_service.get_by_id(pk_value=user_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=user_entity)

    return execute_with_logging("UserEntityService.get_by_id", action)


@router.put(
    "/{user_id}",
    response_model=DataResponse[UserEntityBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_by_id(
    user_id: int = Path(..., gt=0),
    user_entity_data: UserEntityUpdateRequest = ...,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
        # Verify user can only update their own data
        if user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_user_entity = user_entity_service.update_by_id(
            pk_value=user_id, data=user_entity_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_user_entity)

    return execute_with_logging("UserEntityService.update_by_id", action)


@router.patch(
    "/{user_id}",
    response_model=DataResponse[UserEntityBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_by_id(
    user_id: int = Path(..., gt=0),
    user_entity_data: UserEntityUpdateRequest = ...,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
        # Verify user can only update their own data
        if user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_user_entity = user_entity_service.partial_update_by_id(
            pk_value=user_id, data=user_entity_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_user_entity)

    return execute_with_logging("UserEntityService.partial_update_by_id", action)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(
    user_id: int = Path(..., gt=0),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> None:

    def action() -> None:
        # Verify user can only delete their own data
        if user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        user_entity_service.delete_by_id(pk_value=user_id)
        return None

    return execute_with_logging("UserEntityService.delete_by_id", action)

