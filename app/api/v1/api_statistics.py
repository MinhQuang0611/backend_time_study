from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException
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

router = APIRouter(prefix=f"/statistics")

statistics_cache_service: StatisticsCacheService = StatisticsCacheService()
streak_record_service: StreakRecordService = StreakRecordService()


# Statistics Cache endpoints
@router.get(
    "/cache/all",
    response_model=DataResponse[List[StatisticsCacheBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_statistics_cache() -> Any:
    try:
        data, metadata = statistics_cache_service.get_all()
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
) -> Any:
    try:
        data, metadata = statistics_cache_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/cache",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_statistics_cache(cache_data: StatisticsCacheCreateRequest) -> Any:
    try:
        new_cache = statistics_cache_service.create(data=cache_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/cache/{cache_id}",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_statistics_cache_by_id(cache_id: int) -> Any:
    try:
        cache = statistics_cache_service.get_by_id(cache_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/cache/{cache_id}",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_statistics_cache_by_id(cache_id: int, cache_data: StatisticsCacheUpdateRequest) -> Any:
    try:
        updated_cache = statistics_cache_service.update_by_id(cache_id, data=cache_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/cache/{cache_id}",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_statistics_cache_by_id(cache_id: int, cache_data: StatisticsCacheUpdateRequest) -> Any:
    try:
        updated_cache = statistics_cache_service.partial_update_by_id(cache_id, data=cache_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_cache)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/cache/{cache_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_statistics_cache_by_id(cache_id: int) -> None:
    try:
        statistics_cache_service.delete_by_id(cache_id)
    except Exception as e:
        raise CustomException(exception=e)


# Streak Record endpoints
@router.get(
    "/streak/all",
    response_model=DataResponse[List[StreakRecordBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_streak_records() -> Any:
    try:
        data, metadata = streak_record_service.get_all()
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
) -> Any:
    try:
        data, metadata = streak_record_service.get_by_filter(
            pagination_params=pagination_params, sort_params=sort_params
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/streak",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_streak_record(streak_data: StreakRecordCreateRequest) -> Any:
    try:
        new_streak = streak_record_service.create(data=streak_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/streak/{streak_id}",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_streak_record_by_id(streak_id: int) -> Any:
    try:
        streak = streak_record_service.get_by_id(streak_id)
        return DataResponse(http_code=status.HTTP_200_OK, data=streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/streak/{streak_id}",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_streak_record_by_id(streak_id: int, streak_data: StreakRecordUpdateRequest) -> Any:
    try:
        updated_streak = streak_record_service.update_by_id(streak_id, data=streak_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/streak/{streak_id}",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_streak_record_by_id(streak_id: int, streak_data: StreakRecordUpdateRequest) -> Any:
    try:
        updated_streak = streak_record_service.partial_update_by_id(streak_id, data=streak_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/streak/{streak_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_streak_record_by_id(streak_id: int) -> None:
    try:
        streak_record_service.delete_by_id(streak_id)
    except Exception as e:
        raise CustomException(exception=e)

