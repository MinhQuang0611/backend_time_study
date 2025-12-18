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
            print(f"No Facebook friends found for user {user_id}", flush=True)
            return []
        
        print(f"Found {len(facebook_ids)} Facebook friend IDs for user {user_id}: {facebook_ids}", flush=True)
        
        # Tìm users có Facebook account linked
        from app.models.model_external_account import ExternalAccount
        
        # Debug: In ra tất cả external accounts có provider = facebook
        all_fb_accounts = db.session.query(ExternalAccount).filter(
            ExternalAccount.provider == "facebook"
        ).all()
        print(f"All Facebook external accounts in DB: {[(ea.provider_user_id, ea.user_id) for ea in all_fb_accounts]}", flush=True)
        
        # Vấn đề: facebook_friends lưu Facebook ID thực sự (số)
        # external_accounts có thể lưu Firebase UID hoặc Facebook ID
        # 
        # Giải pháp: Tìm user có Facebook friend với Facebook ID đó
        # Logic: Nếu user A có friend với Facebook ID X trong facebook_friends,
        # và user B có external_account với provider=facebook,
        # thì cần tìm cách match X với user B
        #
        # Cách 1: Match trực tiếp nếu provider_user_id = Facebook ID
        facebook_ids_str = [str(fb_id) for fb_id in facebook_ids]
        
        external_accounts = db.session.query(ExternalAccount).filter(
            ExternalAccount.provider == "facebook",
            ExternalAccount.provider_user_id.in_(facebook_ids_str)
        ).all()
        
        print(f"Matching query: provider='facebook', provider_user_id IN {facebook_ids_str}", flush=True)
        print(f"Found {len(external_accounts)} matching external accounts (direct match)", flush=True)
        
        # Cách 2: Nếu không match được, tìm user có Facebook friend với Facebook ID đó
        # và có external_account với provider=facebook (bất kỳ provider_user_id nào)
        # Điều này giả định rằng nếu user có Facebook friend trong danh sách,
        # thì họ có thể là bạn bè (nhưng cần verify thêm)
        if len(external_accounts) == 0:
            print("No direct match found, trying alternative matching...", flush=True)
            # Lấy tất cả users có external_account với provider=facebook
            all_fb_users = [ea.user_id for ea in all_fb_accounts]
            print(f"All users with Facebook external accounts: {all_fb_users}", flush=True)
            
            # Tìm users có Facebook friend với các Facebook IDs này
            # (Có thể là chính các users đó hoặc users khác)
            # Nhưng logic này không chính xác vì không có cách nào biết được
            # user nào có Facebook ID nào nếu không match được
            
            # Tạm thời: Chỉ match trực tiếp
            # Cần fix bằng cách lưu Facebook ID thực sự vào external_accounts
        
        # Lấy user_ids
        friend_user_ids = [ea.user_id for ea in external_accounts]
        
        print(f"Found {len(friend_user_ids)} users with linked Facebook accounts: {friend_user_ids}", flush=True)
        
        # NOTE: Vấn đề hiện tại:
        # - facebook_friends.facebook_user_id = Facebook ID thực sự (từ Facebook Graph API)
        # - external_accounts.provider_user_id = Firebase UID (từ Firebase Auth)
        # 
        # Giải pháp đã áp dụng:
        # - Sửa logic login để lưu Facebook ID thực sự vào external_accounts (nếu có trong token)
        # - Update existing external_accounts khi user đăng nhập lại
        # 
        # Với data cũ: Cần user đăng nhập lại để tự động update, hoặc manual update
        
        # Thêm chính user hiện tại vào danh sách
        if user_id not in friend_user_ids:
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
            
            # Lấy Facebook ID và Facebook picture URL từ facebook_friends
            facebook_user_id = None
            profile_picture_url = user.profile_picture_url  # Default: Firebase URL
            
            # Lấy Facebook ID từ ExternalAccount
            from app.models.model_external_account import ExternalAccount
            fb_account = db.session.query(ExternalAccount).filter(
                ExternalAccount.user_id == friend_user_id,
                ExternalAccount.provider == "facebook"
            ).first()
            
            if fb_account:
                facebook_user_id = fb_account.provider_user_id
                
                # Tìm picture_url từ bảng facebook_friends của current_user
                # (vì facebook_friends lưu thông tin bạn bè của current_user)
                fb_friend = db.session.query(FacebookFriend).filter(
                    FacebookFriend.user_id == user_id,  # Current user's friends list
                    FacebookFriend.facebook_user_id == facebook_user_id
                ).first()
                
                if fb_friend and fb_friend.picture_url:
                    profile_picture_url = fb_friend.picture_url
            
            # Tính score dựa trên metric
            score = LeaderboardService.calculate_score(metrics, metric)
            
            entry = LeaderboardEntry(
                rank=0,  # Sẽ set sau khi sort
                user_id=friend_user_id,
                display_name=user.display_name,
                profile_picture_url=profile_picture_url,
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
        
        # 4. Tính streak từ streak_records (tính trực tiếp từ dữ liệu thực tế)
        from app.models.model_statistics import StreakRecordEntity
        from datetime import datetime, timezone, timedelta
        
        # Lấy tất cả streak records có activity
        if start_timestamp:
            # Nếu có period, chỉ lấy records trong period
            all_records = db.session.query(StreakRecordEntity).filter(
                StreakRecordEntity.user_id == user_id,
                StreakRecordEntity.has_activity == 1,
                StreakRecordEntity.streak_date >= start_timestamp
            ).order_by(StreakRecordEntity.streak_date.desc()).all()
        else:
            # All time - lấy tất cả
            all_records = db.session.query(StreakRecordEntity).filter(
                StreakRecordEntity.user_id == user_id,
                StreakRecordEntity.has_activity == 1
            ).order_by(StreakRecordEntity.streak_date.desc()).all()
        
        if all_records:
            # Tính current_streak: Đếm số ngày liên tiếp từ hôm nay về trước
            current_streak = 0
            today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Tạo dict để lookup nhanh
            active_dates = {}
            for record in all_records:
                record_date = datetime.fromtimestamp(record.streak_date, tz=timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                active_dates[record_date.timestamp()] = True
            
            # Kiểm tra từ hôm nay về trước
            check_date = today
            while check_date.timestamp() in active_dates:
                current_streak += 1
                check_date = check_date - timedelta(days=1)
            
            # Tính best_streak: Tìm chuỗi ngày dài nhất
            sorted_records = sorted(all_records, key=lambda x: x.streak_date)
            best_streak = 0
            if sorted_records:
                current_sequence = 1
                best_sequence = 1
                
                for i in range(1, len(sorted_records)):
                    prev_date = datetime.fromtimestamp(sorted_records[i-1].streak_date, tz=timezone.utc).replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    curr_date = datetime.fromtimestamp(sorted_records[i].streak_date, tz=timezone.utc).replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    
                    days_diff = (curr_date - prev_date).days
                    
                    if days_diff == 1:
                        current_sequence += 1
                        best_sequence = max(best_sequence, current_sequence)
                    else:
                        current_sequence = 1
                
                best_streak = best_sequence
            
            metrics["current_streak"] = current_streak
            metrics["best_streak"] = best_streak
        else:
            metrics["current_streak"] = 0
            metrics["best_streak"] = 0
        
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

