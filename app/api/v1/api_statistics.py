from typing import Any, List, Optional
from fastapi import APIRouter, Depends, status, Query
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
    DailyStatisticsResponse,
    MonthlyStatisticsResponse,
)
from app.services.srv_statistics import StatisticsCacheService, StreakRecordService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity
from pydantic import BaseModel, Field

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


# Statistics từ sessions (tính toán trực tiếp)
@router.get(
    "/daily",
    response_model=DataResponse[DailyStatisticsResponse],
    status_code=status.HTTP_200_OK,
)
def get_daily_statistics(
    date: float = Query(..., description="Timestamp của ngày cần lấy (Unix timestamp - float)"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy statistics theo ngày, tính toán trực tiếp từ sessions, tasks, goals
    """
    try:
        stats = StatisticsCacheService.get_daily_statistics(
            user_id=current_user.user_id,
            date=date
        )
        return DataResponse(
            http_code=status.HTTP_200_OK,
            data=DailyStatisticsResponse(**stats)
        )
    except Exception as e:
        import traceback
        print(f"Error in get_daily_statistics: {str(e)}", flush=True)
        print(traceback.format_exc(), flush=True)
        raise CustomException(exception=e)


@router.get(
    "/monthly",
    response_model=DataResponse[MonthlyStatisticsResponse],
    status_code=status.HTTP_200_OK,
)
def get_monthly_statistics(
    year: int = Query(..., description="Năm (ví dụ: 2024)", ge=2000, le=2100),
    month: int = Query(..., description="Tháng (1-12)", ge=1, le=12),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy statistics theo tháng, tính toán trực tiếp từ sessions, tasks, goals
    """
    try:
        stats = StatisticsCacheService.get_monthly_statistics(
            user_id=current_user.user_id,
            year=year,
            month=month
        )
        return DataResponse(
            http_code=status.HTTP_200_OK,
            data=MonthlyStatisticsResponse(**stats)
        )
    except Exception as e:
        import traceback
        print(f"Error in get_monthly_statistics: {str(e)}", flush=True)
        print(traceback.format_exc(), flush=True)
        raise CustomException(exception=e)


# Streak endpoints - Summary và Current Streak
class StreakSummaryResponse(BaseModel):
    """Response cho streak summary của user"""
    current_streak: int = Field(..., description="Chuỗi ngày hiện tại (integer)")
    best_streak: int = Field(..., description="Chuỗi ngày tốt nhất (integer)")
    total_active_days: int = Field(..., description="Tổng số ngày có hoạt động (integer)")


@router.get(
    "/streak/summary",
    response_model=DataResponse[StreakSummaryResponse],
    status_code=status.HTTP_200_OK,
)
def get_streak_summary(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy thông tin streak summary của user (current_streak, best_streak, total_active_days)
    Tính toán trực tiếp từ streak_records
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StreakRecordEntity
        from datetime import datetime, timezone, timedelta
        
        # Lấy tất cả streak records có activity, sắp xếp theo ngày giảm dần
        all_records = db.session.query(StreakRecordEntity).filter(
            StreakRecordEntity.user_id == current_user.user_id,
            StreakRecordEntity.has_activity == 1
        ).order_by(StreakRecordEntity.streak_date.desc()).all()
        
        total_active_days = len(all_records)
        
        if not all_records:
            return DataResponse(
                http_code=status.HTTP_200_OK,
                data=StreakSummaryResponse(
                    current_streak=0,
                    best_streak=0,
                    total_active_days=0
                )
            )
        
        # Tính current_streak: Đếm số ngày liên tiếp từ hôm nay về trước
        current_streak = 0
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Tạo dict để lookup nhanh: date_timestamp -> True
        active_dates = {}
        for record in all_records:
            record_date = datetime.fromtimestamp(record.streak_date, tz=timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            active_dates[record_date.timestamp()] = True
        
        # Kiểm tra từ hôm nay về trước, đếm số ngày liên tiếp có activity
        check_date = today
        while check_date.timestamp() in active_dates:
            current_streak += 1
            check_date = check_date - timedelta(days=1)
        
        # Tính best_streak: Tìm chuỗi ngày dài nhất
        best_streak = 0
        if all_records:
            # Sắp xếp lại theo ngày tăng dần để tính best streak
            sorted_records = sorted(all_records, key=lambda x: x.streak_date)
            
            current_sequence = 1
            best_sequence = 1
            
            for i in range(1, len(sorted_records)):
                prev_date = datetime.fromtimestamp(sorted_records[i-1].streak_date, tz=timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                curr_date = datetime.fromtimestamp(sorted_records[i].streak_date, tz=timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                
                # Kiểm tra xem có liên tiếp không (chênh lệch 1 ngày)
                days_diff = (curr_date - prev_date).days
                
                if days_diff == 1:
                    # Liên tiếp
                    current_sequence += 1
                    best_sequence = max(best_sequence, current_sequence)
                else:
                    # Không liên tiếp, reset sequence
                    current_sequence = 1
            
            best_streak = best_sequence
        
        summary = StreakSummaryResponse(
            current_streak=current_streak,
            best_streak=best_streak,
            total_active_days=total_active_days
        )
        
        return DataResponse(http_code=status.HTTP_200_OK, data=summary)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/streak/current",
    response_model=DataResponse[StatisticsCacheBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_current_streak_info(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy thông tin streak hiện tại từ statistics_cache (latest cache)
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StatisticsCacheEntity
        
        # Lấy latest cache
        latest_cache = db.session.query(StatisticsCacheEntity).filter(
            StatisticsCacheEntity.user_id == current_user.user_id
        ).order_by(StatisticsCacheEntity.cache_date.desc()).first()
        
        if not latest_cache:
            raise CustomException(exception=ExceptionType.NOT_FOUND)
        
        return DataResponse(http_code=status.HTTP_200_OK, data=latest_cache)
    except Exception as e:
        return CustomException(exception=e)


# Streak Record endpoints
@router.get(
    "/streak/all",
    response_model=DataResponse[List[StreakRecordBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_streak_records(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy tất cả streak records của user
    """
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
    """
    Tạo hoặc cập nhật streak record cho một ngày (upsert)
    So sánh theo ngày, không phải timestamp chính xác
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StreakRecordEntity
        from sqlalchemy import and_, func
        from datetime import datetime, timezone, timedelta
        
        # Add user_id from JWT token
        streak_dict = streak_data.model_dump()
        streak_dict["user_id"] = current_user.user_id
        
        # Normalize streak_date về 00:00:00 của ngày đó để so sánh
        input_date = datetime.fromtimestamp(streak_dict["streak_date"], tz=timezone.utc)
        normalized_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
        normalized_timestamp = normalized_date.timestamp()
        
        # Tính khoảng thời gian của ngày (từ 00:00:00 đến 23:59:59)
        start_of_day = normalized_timestamp
        end_of_day = (normalized_date + timedelta(days=1) - timedelta(seconds=1)).timestamp()
        
        # Tìm record trong cùng ngày (bất kỳ timestamp nào trong ngày đó)
        existing = db.session.query(StreakRecordEntity).filter(
            and_(
                StreakRecordEntity.user_id == current_user.user_id,
                StreakRecordEntity.streak_date >= start_of_day,
                StreakRecordEntity.streak_date <= end_of_day
            )
        ).first()
        
        # Cập nhật streak_date về normalized timestamp để đảm bảo consistency
        streak_dict["streak_date"] = normalized_timestamp
        
        if existing:
            # Nếu đã có thì update
            updated_streak = streak_record_service.update_by_id(
                existing.streak_id, 
                data=streak_dict
            )
            return DataResponse(http_code=status.HTTP_200_OK, data=updated_streak)
        else:
            # Nếu chưa có thì tạo mới
            new_streak = streak_record_service.create(data=streak_dict)
            return DataResponse(http_code=status.HTTP_201_CREATED, data=new_streak)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/streak/by-date",
    response_model=DataResponse[StreakRecordBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_streak_record_by_date(
    date: float = Query(..., description="Timestamp của ngày cần lấy (Unix timestamp - float)"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy streak record theo ngày cụ thể (so sánh theo ngày, không phải timestamp chính xác)
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StreakRecordEntity
        from sqlalchemy import and_
        from datetime import datetime, timezone, timedelta
        
        # Normalize date về 00:00:00 của ngày đó
        input_date = datetime.fromtimestamp(date, tz=timezone.utc)
        normalized_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
        normalized_timestamp = normalized_date.timestamp()
        
        # Tính khoảng thời gian của ngày
        start_of_day = normalized_timestamp
        end_of_day = (normalized_date + timedelta(days=1) - timedelta(seconds=1)).timestamp()
        
        streak = db.session.query(StreakRecordEntity).filter(
            and_(
                StreakRecordEntity.user_id == current_user.user_id,
                StreakRecordEntity.streak_date >= start_of_day,
                StreakRecordEntity.streak_date <= end_of_day
            )
        ).first()
        
        if not streak:
            raise CustomException(exception=ExceptionType.NOT_FOUND)
        
        return DataResponse(http_code=status.HTTP_200_OK, data=streak)
    except Exception as e:
        return CustomException(exception=e)


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


@router.post(
    "/streak/cleanup-duplicates",
    response_model=DataResponse[dict],
    status_code=status.HTTP_200_OK,
)
def cleanup_duplicate_streak_records(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Cleanup duplicate streak records - merge các records trong cùng một ngày thành 1 record
    Giữ lại record có streak_id lớn nhất (mới nhất) và merge dữ liệu
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_statistics import StreakRecordEntity
        from datetime import datetime, timezone, timedelta
        from sqlalchemy import and_
        
        # Lấy tất cả records của user
        all_records = db.session.query(StreakRecordEntity).filter(
            StreakRecordEntity.user_id == current_user.user_id
        ).order_by(StreakRecordEntity.streak_date.desc()).all()
        
        # Group records theo ngày
        records_by_date = {}
        for record in all_records:
            record_date = datetime.fromtimestamp(record.streak_date, tz=timezone.utc)
            normalized_date = record_date.replace(hour=0, minute=0, second=0, microsecond=0)
            date_key = normalized_date.timestamp()
            
            if date_key not in records_by_date:
                records_by_date[date_key] = []
            records_by_date[date_key].append(record)
        
        deleted_count = 0
        merged_count = 0
        
        # Xử lý từng nhóm
        for date_key, records in records_by_date.items():
            if len(records) > 1:
                # Có duplicates, merge lại
                # Sắp xếp theo streak_id giảm dần (mới nhất trước)
                records.sort(key=lambda x: x.streak_id, reverse=True)
                
                # Record đầu tiên (mới nhất) sẽ được giữ lại và merge dữ liệu
                keep_record = records[0]
                
                # Merge dữ liệu từ các records khác
                total_session_count = 0
                total_focus_time = 0
                has_any_activity = 0
                
                for record in records:
                    total_session_count += record.session_count or 0
                    total_focus_time += record.focus_time or 0
                    if record.has_activity == 1:
                        has_any_activity = 1
                
                # Cập nhật record được giữ lại
                keep_record.streak_date = date_key  # Normalize về 00:00:00
                keep_record.session_count = total_session_count
                keep_record.focus_time = total_focus_time
                keep_record.has_activity = has_any_activity
                
                # Xóa các records còn lại
                for record in records[1:]:
                    db.session.delete(record)
                    deleted_count += 1
                
                merged_count += 1
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_200_OK,
            data={
                "message": f"Đã cleanup {merged_count} nhóm duplicate, xóa {deleted_count} records",
                "merged_groups": merged_count,
                "deleted_records": deleted_count
            }
        )
    except Exception as e:
        db.session.rollback()
        return CustomException(exception=e)
