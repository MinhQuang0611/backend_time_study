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

router = APIRouter(prefix=f"/user-entities")


def get_user_entity_service() -> UserEntityService:
    return UserEntityService()


@router.get(
    "/all",
    response_model=DataResponse[List[UserEntityBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all(
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[List[UserEntityBaseResponse]]:
        data, metadata = user_entity_service.get_all()
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
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[List[UserEntityBaseResponse]]:
        data, metadata = user_entity_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
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
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
        new_user_entity = user_entity_service.create(
            data=user_entity_data.model_dump(exclude_none=True)
        )
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_user_entity)

    return execute_with_logging("UserEntityService.create", action)


@router.get(
    "/{user_id}",
    response_model=DataResponse[UserEntityBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    user_id: int = Path(..., gt=0),
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
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
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
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
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> Any:

    def action() -> DataResponse[UserEntityBaseResponse]:
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
    user_entity_service: UserEntityService = Depends(get_user_entity_service),
) -> None:

    def action() -> None:
        user_entity_service.delete_by_id(pk_value=user_id)
        return None

    return execute_with_logging("UserEntityService.delete_by_id", action)

