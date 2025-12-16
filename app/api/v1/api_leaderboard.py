from typing import Any
from fastapi import APIRouter, Depends, Query
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_leaderboard import (
    LeaderboardRequest,
    LeaderboardResponse,
    LeaderboardPeriod,
    LeaderboardMetric
)
from app.services.srv_leaderboard import LeaderboardService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix="/leaderboard")


@router.get(
    "/facebook-friends",
    response_model=DataResponse[LeaderboardResponse],
)
def get_facebook_friends_leaderboard(
    period: LeaderboardPeriod = Query(
        default=LeaderboardPeriod.ALL_TIME,
        description="Period: daily, weekly, monthly, all_time"
    ),
    metric: LeaderboardMetric = Query(
        default=LeaderboardMetric.FOCUS_TIME,
        description="Metric để sort: focus_time, sessions, tasks, streak, best_streak, goals"
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Số lượng entries trả về (1-100)"
    ),
    include_self: bool = Query(
        default=True,
        description="Có bao gồm current user trong leaderboard không"
    ),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy leaderboard theo bạn bè Facebook.
    
    - **period**: daily, weekly, monthly, all_time
    - **metric**: focus_time, sessions, tasks, streak, best_streak, goals
    - **limit**: Số lượng entries (1-100)
    - **include_self**: Có bao gồm current user không
    """
    try:
        result = LeaderboardService.get_leaderboard_data(
            user_id=current_user.user_id,
            period=period,
            metric=metric,
            limit=limit,
            include_self=include_self
        )
        return DataResponse(http_code=200, data=result)
    except Exception as e:
        print(f"Error getting leaderboard: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        raise CustomException(exception=e)


@router.post(
    "/facebook-friends",
    response_model=DataResponse[LeaderboardResponse],
)
def get_facebook_friends_leaderboard_post(
    request: LeaderboardRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy leaderboard theo bạn bè Facebook (POST method).
    
    Cho phép gửi request body với các parameters.
    """
    try:
        result = LeaderboardService.get_leaderboard_data(
            user_id=current_user.user_id,
            period=request.period,
            metric=request.metric,
            limit=request.limit,
            include_self=request.include_self
        )
        return DataResponse(http_code=200, data=result)
    except Exception as e:
        print(f"Error getting leaderboard: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        raise CustomException(exception=e)

