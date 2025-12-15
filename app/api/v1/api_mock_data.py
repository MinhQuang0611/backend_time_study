from typing import Any, List
from fastapi import APIRouter, Depends, status, Query
from faker import Faker
import random
from datetime import datetime, timedelta

from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity
from app.utils import time_utils
from app.core.security import get_password_hash
from fastapi_sqlalchemy import db

router = APIRouter(prefix=f"/mock-data", tags=["MockData"])

fake = Faker()


@router.post(
    "/shop",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_shop_mock_data(
    count: int = Query(default=10, ge=1, le=100, description="Số lượng sản phẩm cần tạo"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho bảng shop
    """
    try:
        from app.models.model_shop import ShopEntity
        
        shop_types = ["theme", "avatar", "pack", "item", "background", "icon"]
        shop_items = []
        
        for _ in range(count):
            shop_item = ShopEntity(
                name=fake.catch_phrase(),
                price=round(random.uniform(1.99, 99.99), 2),
                type=random.choice(shop_types),
            )
            db.session.add(shop_item)
            shop_items.append({
                "shop_id": shop_item.shop_id,
                "name": shop_item.name,
                "price": shop_item.price,
                "type": shop_item.type,
            })
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": f"Đã tạo {count} sản phẩm shop",
                "count": count,
                "items": shop_items,
            }
        )
    except Exception as e:
        db.session.rollback()
        raise CustomException(exception=e)


@router.post(
    "/shop-purchases",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_shop_purchases_mock_data(
    count: int = Query(default=5, ge=1, le=50, description="Số lượng purchase cần tạo"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho bảng shop_purchases (mua sản phẩm cho user hiện tại)
    """
    try:
        from app.models.model_shop import ShopEntity, ShopPurchaseEntity
        
        # Get all shop items
        shop_items = db.session.query(ShopEntity).all()
        if not shop_items:
            raise CustomException(
                exception=ExceptionType.BAD_REQUEST,
                message="Không có sản phẩm nào trong shop. Vui lòng tạo sản phẩm trước."
            )
        
        # Get already purchased items
        purchased_shop_ids = {
            p.shop_id for p in db.session.query(ShopPurchaseEntity).filter(
                ShopPurchaseEntity.user_id == current_user.user_id
            ).all()
        }
        
        # Get available shop items (not purchased yet)
        available_shops = [s for s in shop_items if s.shop_id not in purchased_shop_ids]
        
        if len(available_shops) < count:
            count = len(available_shops)
        
        # Random select shops to purchase
        shops_to_purchase = random.sample(available_shops, count)
        
        purchases = []
        now = time_utils.timestamp_now()
        
        for shop in shops_to_purchase:
            # Random purchase time in the past 30 days
            days_ago = random.randint(0, 30)
            purchased_at = now - (days_ago * 24 * 60 * 60)
            
            purchase = ShopPurchaseEntity(
                user_id=current_user.user_id,
                shop_id=shop.shop_id,
                purchased_at=purchased_at,
            )
            db.session.add(purchase)
            purchases.append({
                "purchase_id": purchase.purchase_id,
                "shop_id": shop.shop_id,
                "shop_name": shop.name,
                "purchased_at": purchased_at,
            })
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": f"Đã tạo {len(purchases)} purchase cho user {current_user.user_id}",
                "count": len(purchases),
                "purchases": purchases,
            }
        )
    except Exception as e:
        db.session.rollback()
        raise CustomException(exception=e)


@router.post(
    "/tasks",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_tasks_mock_data(
    count: int = Query(default=10, ge=1, le=100, description="Số lượng task cần tạo"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho bảng tasks (cho user hiện tại)
    """
    try:
        from app.models.model_task import TaskEntity
        
        priorities = [TaskEntity.PRIORITY_HIGH, TaskEntity.PRIORITY_MEDIUM, TaskEntity.PRIORITY_LOW]
        tasks = []
        now = time_utils.timestamp_now()
        
        for _ in range(count):
            # Random task date in the past 30 days or future 7 days
            days_offset = random.randint(-30, 7)
            task_date = now + (days_offset * 24 * 60 * 60)
            
            is_completed = random.choice([0, 1])
            completed_at = None
            if is_completed:
                completed_at = task_date + random.randint(0, 8 * 60 * 60)  # Completed within 8 hours
            
            task = TaskEntity(
                user_id=current_user.user_id,
                title=fake.sentence(nb_words=4),
                description=fake.text(max_nb_chars=200),
                priority=random.choice(priorities),
                task_date=task_date,
                is_completed=is_completed,
                completed_at=completed_at,
                total_time_spent=random.randint(0, 480) if is_completed else 0,  # 0-8 hours in minutes
                estimated_sessions=random.randint(1, 5),
                actual_sessions=random.randint(0, 5) if is_completed else 0,
                order_index=random.randint(0, 100),
            )
            db.session.add(task)
            tasks.append({
                "task_id": task.task_id,
                "title": task.title,
                "priority": task.priority,
                "is_completed": task.is_completed,
            })
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": f"Đã tạo {count} task cho user {current_user.user_id}",
                "count": count,
                "tasks": tasks,
            }
        )
    except Exception as e:
        db.session.rollback()
        raise CustomException(exception=e)


@router.post(
    "/sessions",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_sessions_mock_data(
    count: int = Query(default=10, ge=1, le=100, description="Số lượng session cần tạo"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho bảng sessions (cho user hiện tại)
    """
    try:
        from app.models.model_session import SessionEntity
        
        session_types = [
            SessionEntity.TYPE_FOCUS_SESSION,
            SessionEntity.TYPE_SHORT_BREAK,
            SessionEntity.TYPE_LONG_BREAK,
        ]
        statuses = [
            SessionEntity.STATUS_COMPLETED,
            SessionEntity.STATUS_CANCELLED,
        ]
        
        sessions = []
        now = time_utils.timestamp_now()
        
        for _ in range(count):
            # Random session date in the past 30 days
            days_ago = random.randint(0, 30)
            session_date = now - (days_ago * 24 * 60 * 60)
            
            session_type = random.choice(session_types)
            duration_minutes = 25 if session_type == SessionEntity.TYPE_FOCUS_SESSION else (
                5 if session_type == SessionEntity.TYPE_SHORT_BREAK else 15
            )
            
            start_time = session_date + random.randint(0, 12 * 60 * 60)  # Random time in the day
            end_time = start_time + (duration_minutes * 60)
            
            session = SessionEntity(
                user_id=current_user.user_id,
                session_date=session_date,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration_minutes,
                session_type=session_type,
                status=random.choice(statuses),
                notes=fake.sentence(nb_words=6) if random.choice([True, False]) else None,
            )
            db.session.add(session)
            sessions.append({
                "session_id": session.session_id,
                "session_type": session.session_type,
                "duration_minutes": session.duration_minutes,
                "status": session.status,
            })
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": f"Đã tạo {count} session cho user {current_user.user_id}",
                "count": count,
                "sessions": sessions,
            }
        )
    except Exception as e:
        db.session.rollback()
        raise CustomException(exception=e)


@router.post(
    "/goals",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_goals_mock_data(
    count: int = Query(default=10, ge=1, le=100, description="Số lượng goal cần tạo"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho bảng goals (cho user hiện tại)
    """
    try:
        from app.models.model_goal import GoalEntity
        
        goals = []
        now = time_utils.timestamp_now()
        
        for _ in range(count):
            # Random goal date in the past 30 days
            days_ago = random.randint(0, 30)
            goal_date = now - (days_ago * 24 * 60 * 60)
            
            target_sessions = random.randint(3, 10)
            completed_sessions = random.randint(0, target_sessions)
            completion_percentage = int((completed_sessions / target_sessions) * 100) if target_sessions > 0 else 0
            is_achieved = 1 if completed_sessions >= target_sessions else 0
            achieved_at = goal_date + random.randint(0, 12 * 60 * 60) if is_achieved else None
            
            goal = GoalEntity(
                user_id=current_user.user_id,
                goal_date=goal_date,
                target_sessions=target_sessions,
                completed_sessions=completed_sessions,
                completion_percentage=completion_percentage,
                is_achieved=is_achieved,
                achieved_at=achieved_at,
            )
            db.session.add(goal)
            goals.append({
                "goal_id": goal.goal_id,
                "goal_date": goal.goal_date,
                "target_sessions": goal.target_sessions,
                "completed_sessions": goal.completed_sessions,
                "is_achieved": goal.is_achieved,
            })
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": f"Đã tạo {count} goal cho user {current_user.user_id}",
                "count": count,
                "goals": goals,
            }
        )
    except Exception as e:
        db.session.rollback()
        raise CustomException(exception=e)


@router.post(
    "/users",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_users_mock_data(
    count: int = Query(default=5, ge=1, le=50, description="Số lượng user cần tạo"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho bảng users
    """
    try:
        from app.models.model_user_entity import UserEntity
        
        users = []
        now = time_utils.timestamp_now()
        
        for _ in range(count):
            email = fake.unique.email()
            display_name = fake.name()
            
            # Random password or None (for Firebase users)
            has_password = random.choice([True, False])
            hashed_password = get_password_hash("password123") if has_password else None
            
            user = UserEntity(
                email=email,
                display_name=display_name,
                profile_picture_url=fake.image_url() if random.choice([True, False]) else None,
                hashed_password=hashed_password,
                last_login=now - random.randint(0, 7 * 24 * 60 * 60),  # Last login in past 7 days
                is_anonymous=0,
            )
            db.session.add(user)
            users.append({
                "user_id": user.user_id,
                "email": user.email,
                "display_name": user.display_name,
                "has_password": has_password,
            })
        
        db.session.commit()
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": f"Đã tạo {count} user",
                "count": count,
                "users": users,
            }
        )
    except Exception as e:
        db.session.rollback()
        raise CustomException(exception=e)


@router.post(
    "/all",
    response_model=DataResponse[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_all_mock_data(
    shop_count: int = Query(default=10, ge=1, le=100, description="Số lượng shop items"),
    tasks_count: int = Query(default=10, ge=1, le=100, description="Số lượng tasks"),
    sessions_count: int = Query(default=10, ge=1, le=100, description="Số lượng sessions"),
    goals_count: int = Query(default=10, ge=1, le=100, description="Số lượng goals"),
    purchases_count: int = Query(default=5, ge=1, le=50, description="Số lượng purchases"),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo fake data cho tất cả các bảng (cho user hiện tại)
    """
    try:
        results = {}
        
        # Generate shop
        shop_result = generate_shop_mock_data(shop_count, current_user)
        results["shop"] = shop_result.data
        
        # Generate purchases
        try:
            purchases_result = generate_shop_purchases_mock_data(purchases_count, current_user)
            results["shop_purchases"] = purchases_result.data
        except Exception as e:
            results["shop_purchases"] = {"error": str(e)}
        
        # Generate tasks
        tasks_result = generate_tasks_mock_data(tasks_count, current_user)
        results["tasks"] = tasks_result.data
        
        # Generate sessions
        sessions_result = generate_sessions_mock_data(sessions_count, current_user)
        results["sessions"] = sessions_result.data
        
        # Generate goals
        goals_result = generate_goals_mock_data(goals_count, current_user)
        results["goals"] = goals_result.data
        
        return DataResponse(
            http_code=status.HTTP_201_CREATED,
            data={
                "message": "Đã tạo fake data cho tất cả các bảng",
                "results": results,
            }
        )
    except Exception as e:
        raise CustomException(exception=e)

