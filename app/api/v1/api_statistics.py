from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_statistics import (
    StatisticsCacheCreateRequest,
    StatisticsCacheUpdateRequest,
    StatisticsCacheBaseResponse,
    StreakRecordCreateRequest,
    StreakRecordUpdateRequest,
    StreakRecordBaseResponse,
)
from app.services.srv_statistics import StatisticsCacheService, StreakRecordService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/statistics")

statistics_cache_service: StatisticsCacheService = StatisticsCacheService()
streak_record_service: StreakRecordService = StreakRecordService()


# Statistics Cache endpoints
@router.get(
    "/cache/all",
    response_model=DataResponse[List[StatisticsCacheBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_statistics_cache(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StatisticsCacheEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        # Filter by user_id
        query = db.session.query(StatisticsCacheEntity).filter(
            StatisticsCacheEntity.user_id == current_user.user_id
        )
        data, metadata = paginate(
            model=StatisticsCacheEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/cache",
    response_model=DataResponse[List[StatisticsCacheBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_statistics_cache_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StatisticsCacheEntity
        from app.utils.paging import paginate
        # Filter by user_id
        query = db.session.query(StatisticsCacheEntity).filter(
            StatisticsCacheEntity.user_id == current_user.user_id
        )
        data, metadata = paginate(
            model=StatisticsCacheEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/cache",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_statistics_cache(
    cache_data: StatisticsCacheCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from app.utils import time_utils
        # Add user_id from JWT token
        cache_dict = cache_data.model_dump()
        cache_dict["user_id"] = current_user.user_id
        cache_dict["cached_at"] = time_utils.timestamp_now()
        new_cache = statistics_cache_service.create(data=cache_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/cache/{cache_id}",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_statistics_cache_by_id(
    cache_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        cache = statistics_cache_service.get_by_id(cache_id)
        # Verify cache belongs to current user
        if cache.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/cache/{cache_id}",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_statistics_cache_by_id(
    cache_id: int,
    cache_data: StatisticsCacheUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        cache = statistics_cache_service.get_by_id(cache_id)
        # Verify cache belongs to current user
        if cache.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_cache = statistics_cache_service.update_by_id(
            cache_id, data=cache_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/cache/{cache_id}",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_statistics_cache_by_id(
    cache_id: int,
    cache_data: StatisticsCacheUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        cache = statistics_cache_service.get_by_id(cache_id)
        # Verify cache belongs to current user
        if cache.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_cache = statistics_cache_service.partial_update_by_id(
            cache_id, data=cache_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/cache/{cache_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_statistics_cache_by_id(
    cache_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        cache = statistics_cache_service.get_by_id(cache_id)
        # Verify cache belongs to current user
        if cache.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        statistics_cache_service.delete_by_id(cache_id)
    except Exception as e:
        raise CustomException(exception=e)


# Streak Record endpoints
@router.get(
    "/streak/all",
    response_model=DataResponse[List[StreakRecordBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_streak_records(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StreakRecordEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        # Filter by user_id
        query = db.session.query(StreakRecordEntity).filter(
            StreakRecordEntity.user_id == current_user.user_id
        )
        data, metadata = paginate(
            model=StreakRecordEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/streak",
    response_model=DataResponse[List[StreakRecordBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_streak_records_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StreakRecordEntity
        from app.utils.paging import paginate
        # Filter by user_id
        query = db.session.query(StreakRecordEntity).filter(
            StreakRecordEntity.user_id == current_user.user_id
        )
        data, metadata = paginate(
            model=StreakRecordEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/streak",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_streak_record(
    streak_data: StreakRecordCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        # Add user_id from JWT token
        streak_dict = streak_data.model_dump()
        streak_dict["user_id"] = current_user.user_id
        new_streak = streak_record_service.create(data=streak_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/streak/{streak_id}",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_streak_record_by_id(
    streak_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        streak = streak_record_service.get_by_id(streak_id)
        # Verify streak belongs to current user
        if streak.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/streak/{streak_id}",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_streak_record_by_id(
    streak_id: int,
    streak_data: StreakRecordUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        streak = streak_record_service.get_by_id(streak_id)
        # Verify streak belongs to current user
        if streak.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_streak = streak_record_service.update_by_id(
            streak_id, data=streak_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/streak/{streak_id}",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_streak_record_by_id(
    streak_id: int,
    streak_data: StreakRecordUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        streak = streak_record_service.get_by_id(streak_id)
        # Verify streak belongs to current user
        if streak.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_streak = streak_record_service.partial_update_by_id(
            streak_id, data=streak_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/streak/{streak_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_streak_record_by_id(
    streak_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        streak = streak_record_service.get_by_id(streak_id)
        # Verify streak belongs to current user
        if streak.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        streak_record_service.delete_by_id(streak_id)
    except Exception as e:
        raise CustomException(exception=e)
