from typing import Any, List, Optional
from fastapi import APIRouter, Depends, status, Query
from datetime import datetime, timedelta, timezone
from app.utils.exception_handler import CustomException, ExceptionType
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
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/tasks")

task_service: TaskService = TaskService()
task_session_service: TaskSessionService = TaskSessionService()


# Task endpoints
@router.get(
    "/all",
    response_model=DataResponse[List[TaskBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired())
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        # Filter by user_id
        query = db.session.query(TaskEntity).filter(TaskEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=TaskEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
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
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        from app.utils.paging import paginate
        # Filter by user_id
        query = db.session.query(TaskEntity).filter(TaskEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=TaskEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/filter-by-date",
    response_model=DataResponse[List[TaskBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_tasks_by_date_filter(
    filter_type: str = Query(..., description="Loại lọc: 'day', 'week', hoặc 'month'"),
    date: Optional[float] = Query(None, description="Timestamp của ngày cần lọc (nếu không có sẽ dùng ngày hiện tại)"),
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy danh sách task với lọc theo ngày, tuần, hoặc tháng
    
    - filter_type: 'day' (ngày), 'week' (tuần), hoặc 'month' (tháng)
    - date: Timestamp của ngày cần lọc (optional, mặc định là ngày hiện tại)
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        from app.utils.paging import paginate
        
        # Validate filter_type
        if filter_type not in ['day', 'week', 'month']:
            raise CustomException(
                http_code=400,
                message="filter_type phải là 'day', 'week', hoặc 'month'"
            )
        
        # Xác định ngày cần lọc
        if date is None:
            # Dùng ngày hiện tại
            target_date = datetime.now(timezone.utc)
        else:
            target_date = datetime.fromtimestamp(date, tz=timezone.utc)
        
        # Tính toán khoảng thời gian dựa trên filter_type
        if filter_type == 'day':
            # Lọc theo ngày: từ 00:00:00 đến 23:59:59 của ngày đó
            start_datetime = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_datetime = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif filter_type == 'week':
            # Lọc theo tuần: từ thứ 2 đến chủ nhật của tuần chứa ngày đó
            # Tìm thứ 2 của tuần (Monday = 0)
            days_since_monday = target_date.weekday()
            start_datetime = (target_date - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_datetime = (start_datetime + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999)
        else:  # month
            # Lọc theo tháng: từ ngày 1 đến ngày cuối cùng của tháng
            start_datetime = target_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Tìm ngày cuối cùng của tháng
            if target_date.month == 12:
                next_month = start_datetime.replace(year=target_date.year + 1, month=1)
            else:
                next_month = start_datetime.replace(month=target_date.month + 1)
            end_datetime = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Chuyển đổi sang timestamp
        start_timestamp = start_datetime.timestamp()
        end_timestamp = end_datetime.timestamp()
        
        # Query với filter theo user_id và khoảng thời gian
        query = db.session.query(TaskEntity).filter(
            TaskEntity.user_id == current_user.user_id,
            TaskEntity.task_date >= start_timestamp,
            TaskEntity.task_date <= end_timestamp
        )
        
        data, metadata = paginate(
            model=TaskEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(
    task_data: TaskCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        # Add user_id from JWT token
        task_dict = task_data.model_dump()
        task_dict["user_id"] = current_user.user_id
        new_task = task_service.create(data=task_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_task)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{task_id}",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    task_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        task = task_service.get_by_id(task_id)
        # Verify task belongs to current user
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=task)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/{task_id}",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_by_id(
    task_id: int,
    task_data: TaskUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        task = task_service.get_by_id(task_id)
        # Verify task belongs to current user
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_task = task_service.update_by_id(task_id, data=task_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/{task_id}",
    response_model=DataResponse[TaskBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_by_id(
    task_id: int,
    task_data: TaskUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        task = task_service.get_by_id(task_id)
        # Verify task belongs to current user
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_task = task_service.partial_update_by_id(task_id, data=task_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(
    task_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        task = task_service.get_by_id(task_id)
        # Verify task belongs to current user
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        task_service.delete_by_id(task_id)
    except Exception as e:
        raise CustomException(exception=e)


# Task Session endpoints
@router.get(
    "/sessions/all",
    response_model=DataResponse[List[TaskSessionBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_task_sessions(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskSessionEntity, TaskEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        # Filter by user_id through task
        query = db.session.query(TaskSessionEntity).join(
            TaskEntity, TaskSessionEntity.task_id == TaskEntity.task_id
        ).filter(TaskEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=TaskSessionEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
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
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskSessionEntity, TaskEntity
        from app.utils.paging import paginate
        # Filter by user_id through task
        query = db.session.query(TaskSessionEntity).join(
            TaskEntity, TaskSessionEntity.task_id == TaskEntity.task_id
        ).filter(TaskEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=TaskSessionEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/sessions",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_task_session(
    task_session_data: TaskSessionCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        # Verify task belongs to current user
        task = db.session.query(TaskEntity).filter(
            TaskEntity.task_id == task_session_data.task_id
        ).first()
        if not task:
            raise CustomException(exception=ExceptionType.NOT_FOUND)
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        new_task_session = task_session_service.create(data=task_session_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/sessions/{task_session_id}",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_task_session_by_id(
    task_session_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        task_session = task_session_service.get_by_id(task_session_id)
        # Verify task belongs to current user
        task = db.session.query(TaskEntity).filter(
            TaskEntity.task_id == task_session.task_id
        ).first()
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/sessions/{task_session_id}",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_task_session_by_id(
    task_session_id: int,
    task_session_data: TaskSessionUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        task_session = task_session_service.get_by_id(task_session_id)
        # Verify task belongs to current user
        task = db.session.query(TaskEntity).filter(
            TaskEntity.task_id == task_session.task_id
        ).first()
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_task_session = task_session_service.update_by_id(
            task_session_id, data=task_session_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/sessions/{task_session_id}",
    response_model=DataResponse[TaskSessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_task_session_by_id(
    task_session_id: int,
    task_session_data: TaskSessionUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        task_session = task_session_service.get_by_id(task_session_id)
        # Verify task belongs to current user
        task = db.session.query(TaskEntity).filter(
            TaskEntity.task_id == task_session.task_id
        ).first()
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_task_session = task_session_service.partial_update_by_id(
            task_session_id, data=task_session_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_task_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/sessions/{task_session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_session_by_id(
    task_session_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_task import TaskEntity
        task_session = task_session_service.get_by_id(task_session_id)
        # Verify task belongs to current user
        task = db.session.query(TaskEntity).filter(
            TaskEntity.task_id == task_session.task_id
        ).first()
        if task.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        task_session_service.delete_by_id(task_session_id)
    except Exception as e:
        raise CustomException(exception=e)

