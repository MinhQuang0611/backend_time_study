from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_goal import (
    GoalCreateRequest,
    GoalUpdateRequest,
    GoalBaseResponse,
)
from app.services.srv_goal import GoalService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/goals")

goal_service: GoalService = GoalService()


@router.get(
    "/all",
    response_model=DataResponse[List[GoalBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired())
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_goal import GoalEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        query = db.session.query(GoalEntity).filter(GoalEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=GoalEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
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
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_goal import GoalEntity
        from app.utils.paging import paginate
        query = db.session.query(GoalEntity).filter(GoalEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=GoalEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(
    goal_data: GoalCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        goal_dict = goal_data.model_dump()
        goal_dict["user_id"] = current_user.user_id
        new_goal = goal_service.create(data=goal_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{goal_id}",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    goal_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        goal = goal_service.get_by_id(goal_id)
        if goal.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/{goal_id}",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_by_id(
    goal_id: int,
    goal_data: GoalUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        goal = goal_service.get_by_id(goal_id)
        if goal.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_goal = goal_service.update_by_id(goal_id, data=goal_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/{goal_id}",
    response_model=DataResponse[GoalBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_by_id(
    goal_id: int,
    goal_data: GoalUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        goal = goal_service.get_by_id(goal_id)
        if goal.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_goal = goal_service.partial_update_by_id(goal_id, data=goal_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_goal)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(
    goal_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        goal = goal_service.get_by_id(goal_id)
        if goal.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        goal_service.delete_by_id(goal_id)
    except Exception as e:
        raise CustomException(exception=e)

