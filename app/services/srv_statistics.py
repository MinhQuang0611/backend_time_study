from fastapi_sqlalchemy import db
from app.models.model_statistics import StatisticsCacheEntity, StreakRecordEntity
from app.models.model_session import SessionEntity
from app.models.model_task import TaskEntity
from app.models.model_goal import GoalEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from typing import Any, Dict, Optional
from sqlalchemy import func, and_, case
from datetime import datetime, timezone, timedelta


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

    @staticmethod
    def calculate_statistics_from_sessions(
        user_id: int,
        start_timestamp: float,
        end_timestamp: float
    ) -> Dict[str, Any]:
        """
        Tính toán statistics từ sessions, tasks, goals trong khoảng thời gian
        
        Args:
            user_id: ID của user
            start_timestamp: Timestamp bắt đầu (inclusive)
            end_timestamp: Timestamp kết thúc (inclusive)
            
        Returns:
            Dict chứa các metrics
        """
        # 1. Tính sessions và focus time
        sessions_query = db.session.query(
            func.sum(
                case(
                    (SessionEntity.session_type == SessionEntity.TYPE_FOCUS_SESSION, SessionEntity.duration_minutes),
                    else_=0
                )
            ).label("total_focus_time"),
            func.sum(
                case(
                    (SessionEntity.session_type.in_([SessionEntity.TYPE_SHORT_BREAK, SessionEntity.TYPE_LONG_BREAK]), SessionEntity.duration_minutes),
                    else_=0
                )
            ).label("total_break_time"),
            func.count(
                case(
                    (SessionEntity.session_type == SessionEntity.TYPE_FOCUS_SESSION, SessionEntity.session_id),
                    else_=None
                )
            ).label("total_sessions")
        ).filter(
            SessionEntity.user_id == user_id,
            SessionEntity.status == SessionEntity.STATUS_COMPLETED,
            SessionEntity.session_date >= start_timestamp,
            SessionEntity.session_date <= end_timestamp
        ).first()
        
        # Xử lý trường hợp không có dữ liệu
        if sessions_query is None:
            total_focus_time = 0
            total_break_time = 0
            total_sessions = 0
        else:
            total_focus_time = int(sessions_query.total_focus_time or 0)
            total_break_time = int(sessions_query.total_break_time or 0)
            total_sessions = int(sessions_query.total_sessions or 0)
        
        # 2. Tính completed tasks (chỉ tính những task có completed_at trong khoảng thời gian)
        tasks_query = db.session.query(
            func.count(TaskEntity.task_id)
        ).filter(
            TaskEntity.user_id == user_id,
            TaskEntity.is_completed == 1,
            TaskEntity.completed_at.isnot(None),
            TaskEntity.completed_at >= start_timestamp,
            TaskEntity.completed_at <= end_timestamp
        ).scalar()
        
        completed_tasks = int(tasks_query or 0)
        
        # 3. Tính goals achieved (chỉ tính những goal có achieved_at trong khoảng thời gian)
        goals_query = db.session.query(
            func.count(GoalEntity.goal_id)
        ).filter(
            GoalEntity.user_id == user_id,
            GoalEntity.is_achieved == 1,
            GoalEntity.achieved_at.isnot(None),
            GoalEntity.achieved_at >= start_timestamp,
            GoalEntity.achieved_at <= end_timestamp
        ).scalar()
        
        goal_achieved = int(goals_query or 0)
        
        return {
            "total_sessions": total_sessions,
            "total_focus_time": total_focus_time,
            "total_break_time": total_break_time,
            "completed_tasks": completed_tasks,
            "goal_achieved": goal_achieved
        }

    @staticmethod
    def get_daily_statistics(user_id: int, date: float) -> Dict[str, Any]:
        """
        Lấy statistics theo ngày
        
        Args:
            user_id: ID của user
            date: Timestamp của ngày (bất kỳ thời điểm nào trong ngày, có thể là seconds hoặc milliseconds)
            
        Returns:
            Dict chứa statistics của ngày đó
        """
        # Kiểm tra xem date là milliseconds hay seconds
        # Nếu > 1e10 thì là milliseconds, cần convert về seconds
        if date > 1e10:
            date = date / 1000.0
        
        # Normalize về 00:00:00 của ngày đó
        input_date = datetime.fromtimestamp(date, tz=timezone.utc)
        start_of_day = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
        
        start_timestamp = start_of_day.timestamp()
        end_timestamp = end_of_day.timestamp()
        
        # Convert sang milliseconds để so sánh với session_date trong DB
        start_timestamp_ms = start_timestamp * 1000
        end_timestamp_ms = end_timestamp * 1000
        
        stats = StatisticsCacheService.calculate_statistics_from_sessions(
            user_id, start_timestamp_ms, end_timestamp_ms
        )
        
        # Thêm thông tin về ngày
        stats["date"] = start_timestamp
        stats["date_string"] = start_of_day.strftime("%Y-%m-%d")
        
        return stats

    @staticmethod
    def get_monthly_statistics(user_id: int, year: int, month: int) -> Dict[str, Any]:
        """
        Lấy statistics theo tháng
        
        Args:
            user_id: ID của user
            year: Năm (ví dụ: 2024)
            month: Tháng (1-12)
            
        Returns:
            Dict chứa statistics của tháng đó
        """
        # Tính start và end của tháng
        start_of_month = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc) - timedelta(seconds=1)
        else:
            end_of_month = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=timezone.utc) - timedelta(seconds=1)
        
        start_timestamp = start_of_month.timestamp()
        end_timestamp = end_of_month.timestamp()
        
        # Convert sang milliseconds để so sánh với session_date trong DB
        start_timestamp_ms = start_timestamp * 1000
        end_timestamp_ms = end_timestamp * 1000
        
        stats = StatisticsCacheService.calculate_statistics_from_sessions(
            user_id, start_timestamp_ms, end_timestamp_ms
        )
        
        # Thêm thông tin về tháng
        stats["year"] = year
        stats["month"] = month
        stats["month_string"] = start_of_month.strftime("%Y-%m")
        
        return stats


class StreakRecordService(BaseService[StreakRecordEntity]):

    def __init__(self):
        super().__init__(StreakRecordEntity)

