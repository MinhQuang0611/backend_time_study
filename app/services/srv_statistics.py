from fastapi_sqlalchemy import db
from app.models.model_statistics import StatisticsCacheEntity, StreakRecordEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from typing import Any, Dict


class StatisticsCacheService(BaseService[StatisticsCacheEntity]):

    def __init__(self):
        super().__init__(StatisticsCacheEntity)

    def create(self, data: Dict[str, Any]) -> StatisticsCacheEntity:
        """
        Create a new StatisticsCacheEntity with duplicate check for user_id + cache_date + cache_type
        """
        # Check unique constraint: user_id + cache_date + cache_type
        if "user_id" in data and "cache_date" in data and "cache_type" in data:
            existing = self.check_duplicate({
                "user_id": data["user_id"],
                "cache_date": data["cache_date"],
                "cache_type": data["cache_type"]
            })
            if existing:
                raise CustomException(
                    exception=ExceptionType.DUPLICATE_ENTRY,
                    message=f"Statistics cache for user {data['user_id']} on date {data['cache_date']} with type {data['cache_type']} already exists"
                )
        
        return super().create(data)


class StreakRecordService(BaseService[StreakRecordEntity]):

    def __init__(self):
        super().__init__(StreakRecordEntity)

