from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_task import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskBaseResponse,
    TaskSessionCreateRequest,
    TaskSessionUpdateRequest,
    TaskSessionBaseResponse,
)
from app.services.srv_task import TaskService, TaskSessionService

router = APIRouter(prefix=f"/tasks")

task_service: TaskService = TaskService()
task_session_service: TaskSessionService = TaskSessionService()


# Task endpoints
@router.get(
    "/all",
    response_model=DataResponse[List[TaskBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all() -> Any:
    try:
        data, metadata = task_service.get_all()
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "",
    response_model=DataResponse[List[TaskBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
) -> Any:
    try:
        data, metadata = task_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(task_data: TaskCreateRequest) -> Any:
    try:
        new_task = task_service.create(data=task_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_task)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{task_id}",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(task_id: int) -> Any:
    try:
        task = task_service.get_by_id(task_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=task)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/{task_id}",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_by_id(task_id: int, task_data: TaskUpdateRequest) -> Any:
    try:
        updated_task = task_service.update_by_id(task_id, data=task_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/{task_id}",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_by_id(task_id: int, task_data: TaskUpdateRequest) -> Any:
    try:
        updated_task = task_service.partial_update_by_id(task_id, data=task_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(task_id: int) -> None:
    try:
        task_service.delete_by_id(task_id)
    except Exception as e:
        raise CustomException(exception=e)


# Task Session endpoints
@router.get(
    "/sessions/all",
    response_model=DataResponse[List[TaskSessionBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_task_sessions() -> Any:
    try:
        data, metadata = task_session_service.get_all()
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/sessions",
    response_model=DataResponse[List[TaskSessionBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_task_sessions_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
) -> Any:
    try:
        data, metadata = task_session_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/sessions",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_task_session(task_session_data: TaskSessionCreateRequest) -> Any:
    try:
        new_task_session = task_session_service.create(data=task_session_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/sessions/{task_session_id}",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_task_session_by_id(task_session_id: int) -> Any:
    try:
        task_session = task_session_service.get_by_id(task_session_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/sessions/{task_session_id}",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_task_session_by_id(task_session_id: int, task_session_data: TaskSessionUpdateRequest) -> Any:
    try:
        updated_task_session = task_session_service.update_by_id(task_session_id, data=task_session_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/sessions/{task_session_id}",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_task_session_by_id(task_session_id: int, task_session_data: TaskSessionUpdateRequest) -> Any:
    try:
        updated_task_session = task_session_service.partial_update_by_id(task_session_id, data=task_session_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/sessions/{task_session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_session_by_id(task_session_id: int) -> None:
    try:
        task_session_service.delete_by_id(task_session_id)
    except Exception as e:
        raise CustomException(exception=e)

