from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session
from fastapi_sqlalchemy import db
from fastapi import HTTPException

from app.models.model_user_entity import UserEntity
from app.models.model_facebook_friend import FacebookFriend
from app.models.model_statistics import StatisticsCacheEntity
from app.models.model_session import SessionEntity
from app.models.model_task import TaskEntity
from app.models.model_goal import GoalEntity
from app.schemas.sche_leaderboard import (
    LeaderboardEntry,
    LeaderboardResponse,
    LeaderboardPeriod,
    LeaderboardMetric
)
from app.utils import time_utils


class LeaderboardService:
    """Service để tính toán leaderboard"""
    
    @staticmethod
    def get_facebook_friends_user_ids(user_id: int) -> List[int]:
        """Lấy danh sách user_id của bạn bè Facebook"""
        friends = db.session.query(FacebookFriend).filter(
            FacebookFriend.user_id == user_id
        ).all()
        
        # Lấy Facebook IDs
        facebook_ids = [f.facebook_user_id for f in friends]
        
        if not facebook_ids:
            return []
        
        # Tìm users có Facebook account linked
        from app.models.model_external_account import ExternalAccount
        external_accounts = db.session.query(ExternalAccount).filter(
            ExternalAccount.provider == "facebook",
            ExternalAccount.provider_user_id.in_(facebook_ids)
        ).all()
        
        # Lấy user_ids
        friend_user_ids = [ea.user_id for ea in external_accounts]
        
        # Thêm chính user hiện tại vào danh sách
        friend_user_ids.append(user_id)
        
        return friend_user_ids
    
    @staticmethod
    def get_period_timestamp(period: LeaderboardPeriod) -> Optional[float]:
        """Lấy timestamp bắt đầu của period"""
        now = datetime.now()
        
        if period == LeaderboardPeriod.DAILY:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == LeaderboardPeriod.WEEKLY:
            # Start of week (Monday)
            days_since_monday = now.weekday()
            start = (now - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif period == LeaderboardPeriod.MONTHLY:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:  # ALL_TIME
            return None
        
        return start.timestamp()
    
    @staticmethod
    def get_leaderboard_data(
        user_id: int,
        period: LeaderboardPeriod = LeaderboardPeriod.ALL_TIME,
        metric: LeaderboardMetric = LeaderboardMetric.FOCUS_TIME,
        limit: int = 50,
        include_self: bool = True
    ) -> LeaderboardResponse:
        """
        Lấy leaderboard theo bạn bè Facebook
        
        Args:
            user_id: ID của user hiện tại
            period: Period (daily, weekly, monthly, all_time)
            metric: Metric để sort
            limit: Số lượng entries
            include_self: Có bao gồm current user không
            
        Returns:
            LeaderboardResponse
        """
        # 1. Lấy danh sách user_ids của bạn bè Facebook
        friend_user_ids = LeaderboardService.get_facebook_friends_user_ids(user_id)
        
        if not friend_user_ids:
            return LeaderboardResponse(
                period=period.value,
                metric=metric.value,
                current_user_rank=None,
                total_participants=0,
                entries=[],
                note="Bạn chưa có bạn bè Facebook nào sử dụng app này. Hãy mời bạn bè tham gia!"
            )
        
        # 2. Lấy timestamp bắt đầu nếu có period
        start_timestamp = LeaderboardService.get_period_timestamp(period)
        
        # 3. Tính toán metrics cho từng user
        leaderboard_entries = []
        
        for friend_user_id in friend_user_ids:
            # Skip current user nếu không include_self
            if not include_self and friend_user_id == user_id:
                continue
            
            # Lấy thông tin user
            user = db.session.query(UserEntity).filter(
                UserEntity.user_id == friend_user_id
            ).first()
            
            if not user:
                continue
            
            # Tính metrics
            metrics = LeaderboardService.calculate_user_metrics(
                friend_user_id,
                start_timestamp,
                period
            )
            
            # Lấy Facebook ID nếu có
            facebook_user_id = None
            if friend_user_id != user_id:
                from app.models.model_external_account import ExternalAccount
                fb_account = db.session.query(ExternalAccount).filter(
                    ExternalAccount.user_id == friend_user_id,
                    ExternalAccount.provider == "facebook"
                ).first()
                if fb_account:
                    facebook_user_id = fb_account.provider_user_id
            
            # Tính score dựa trên metric
            score = LeaderboardService.calculate_score(metrics, metric)
            
            entry = LeaderboardEntry(
                rank=0,  # Sẽ set sau khi sort
                user_id=friend_user_id,
                display_name=user.display_name,
                profile_picture_url=user.profile_picture_url,
                facebook_user_id=facebook_user_id,
                is_current_user=(friend_user_id == user_id),
                focus_time=metrics.get("focus_time", 0),
                sessions=metrics.get("sessions", 0),
                tasks=metrics.get("tasks", 0),
                current_streak=metrics.get("current_streak", 0),
                best_streak=metrics.get("best_streak", 0),
                goals=metrics.get("goals", 0),
                score=score
            )
            
            leaderboard_entries.append(entry)
        
        # 4. Sort theo score (descending)
        leaderboard_entries.sort(key=lambda x: x.score, reverse=True)
        
        # 5. Set rank
        for idx, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = idx
        
        # 6. Limit số lượng
        leaderboard_entries = leaderboard_entries[:limit]
        
        # 7. Tìm rank của current user
        current_user_rank = None
        if include_self:
            for entry in leaderboard_entries:
                if entry.is_current_user:
                    current_user_rank = entry.rank
                    break
        
        return LeaderboardResponse(
            period=period.value,
            metric=metric.value,
            current_user_rank=current_user_rank,
            total_participants=len(leaderboard_entries),
            entries=leaderboard_entries,
            note=None
        )
    
    @staticmethod
    def calculate_user_metrics(user_id: int, start_timestamp: Optional[float] = None, period: Optional[LeaderboardPeriod] = None) -> Dict[str, int]:
        """Tính toán metrics cho một user"""
        metrics = {
            "focus_time": 0,
            "sessions": 0,
            "tasks": 0,
            "current_streak": 0,
            "best_streak": 0,
            "goals": 0
        }
        
        # Nếu có start_timestamp, filter theo thời gian
        time_filter = []
        if start_timestamp:
            time_filter.append(SessionEntity.session_date >= start_timestamp)
        
        # 1. Tính focus_time và sessions từ sessions
        if start_timestamp:
            sessions_query = db.session.query(
                func.sum(SessionEntity.duration_minutes).label("total_time"),
                func.count(SessionEntity.session_id).label("total_sessions")
            ).filter(
                SessionEntity.user_id == user_id,
                SessionEntity.status == SessionEntity.STATUS_COMPLETED,
                SessionEntity.session_type == SessionEntity.TYPE_FOCUS_SESSION,
                SessionEntity.session_date >= start_timestamp
            ).first()
        else:
            sessions_query = db.session.query(
                func.sum(SessionEntity.duration_minutes).label("total_time"),
                func.count(SessionEntity.session_id).label("total_sessions")
            ).filter(
                SessionEntity.user_id == user_id,
                SessionEntity.status == SessionEntity.STATUS_COMPLETED,
                SessionEntity.session_type == SessionEntity.TYPE_FOCUS_SESSION
            ).first()
        
        if sessions_query:
            metrics["focus_time"] = int(sessions_query.total_time or 0)
            metrics["sessions"] = int(sessions_query.total_sessions or 0)
        
        # 2. Tính tasks completed
        if start_timestamp:
            tasks_query = db.session.query(
                func.count(TaskEntity.task_id)
            ).filter(
                TaskEntity.user_id == user_id,
                TaskEntity.is_completed == 1,
                TaskEntity.completed_at >= start_timestamp
            ).scalar()
        else:
            tasks_query = db.session.query(
                func.count(TaskEntity.task_id)
            ).filter(
                TaskEntity.user_id == user_id,
                TaskEntity.is_completed == 1
            ).scalar()
        
        metrics["tasks"] = int(tasks_query or 0)
        
        # 3. Tính goals achieved
        if start_timestamp:
            goals_query = db.session.query(
                func.count(GoalEntity.goal_id)
            ).filter(
                GoalEntity.user_id == user_id,
                GoalEntity.is_achieved == 1,
                GoalEntity.achieved_at >= start_timestamp
            ).scalar()
        else:
            goals_query = db.session.query(
                func.count(GoalEntity.goal_id)
            ).filter(
                GoalEntity.user_id == user_id,
                GoalEntity.is_achieved == 1
            ).scalar()
        
        metrics["goals"] = int(goals_query or 0)
        
        # 4. Lấy streak từ statistics_cache (lấy latest)
        # Nếu có period, lấy cache theo period, nếu không lấy latest
        if start_timestamp and period:
            # Lấy cache theo period
            if period == LeaderboardPeriod.DAILY:
                cache_type = StatisticsCacheEntity.TYPE_DAILY
            elif period == LeaderboardPeriod.WEEKLY:
                cache_type = StatisticsCacheEntity.TYPE_DAILY  # Weekly dùng daily cache
            elif period == LeaderboardPeriod.MONTHLY:
                cache_type = StatisticsCacheEntity.TYPE_MONTHLY
            else:
                cache_type = StatisticsCacheEntity.TYPE_YEARLY
            
            latest_cache = db.session.query(StatisticsCacheEntity).filter(
                StatisticsCacheEntity.user_id == user_id,
                StatisticsCacheEntity.cache_type == cache_type,
                StatisticsCacheEntity.cache_date >= start_timestamp
            ).order_by(StatisticsCacheEntity.cache_date.desc()).first()
        else:
            # Lấy latest cache bất kỳ
            latest_cache = db.session.query(StatisticsCacheEntity).filter(
                StatisticsCacheEntity.user_id == user_id
            ).order_by(StatisticsCacheEntity.cache_date.desc()).first()
        
        if latest_cache:
            metrics["current_streak"] = latest_cache.current_streak or 0
            metrics["best_streak"] = latest_cache.best_streak or 0
        
        return metrics
    
    @staticmethod
    def calculate_score(metrics: Dict[str, int], metric: LeaderboardMetric) -> float:
        """Tính score dựa trên metric được chọn"""
        if metric == LeaderboardMetric.FOCUS_TIME:
            return float(metrics.get("focus_time", 0))
        elif metric == LeaderboardMetric.SESSIONS:
            return float(metrics.get("sessions", 0))
        elif metric == LeaderboardMetric.TASKS:
            return float(metrics.get("tasks", 0))
        elif metric == LeaderboardMetric.STREAK:
            return float(metrics.get("current_streak", 0))
        elif metric == LeaderboardMetric.BEST_STREAK:
            return float(metrics.get("best_streak", 0))
        elif metric == LeaderboardMetric.GOALS:
            return float(metrics.get("goals", 0))
        else:
            return 0.0

