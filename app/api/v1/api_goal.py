from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_goal import (
    GoalCreateRequest,
    GoalUpdateRequest,
    GoalBaseResponse,
)
from app.services.srv_goal import GoalService

router = APIRouter(prefix=f"/goals")

goal_service: GoalService = GoalService()


@router.get(
    "/all",
    response_model=DataResponse[List[GoalBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all() -> Any:
    try:
        data, metadata = goal_service.get_all()
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "",
    response_model=DataResponse[List[GoalBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
) -> Any:
    try:
        data, metadata = goal_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(goal_data: GoalCreateRequest) -> Any:
    try:
        new_goal = goal_service.create(data=goal_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{goal_id}",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(goal_id: int) -> Any:
    try:
        goal = goal_service.get_by_id(goal_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/{goal_id}",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_by_id(goal_id: int, goal_data: GoalUpdateRequest) -> Any:
    try:
        updated_goal = goal_service.update_by_id(goal_id, data=goal_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/{goal_id}",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_by_id(goal_id: int, goal_data: GoalUpdateRequest) -> Any:
    try:
        updated_goal = goal_service.partial_update_by_id(goal_id, data=goal_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(goal_id: int) -> None:
    try:
        goal_service.delete_by_id(goal_id)
    except Exception as e:
        raise CustomException(exception=e)

