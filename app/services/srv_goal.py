from fastapi_sqlalchemy import db
from app.models.model_goal import GoalEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from typing import Any, Dict


class GoalService(BaseService[GoalEntity]):

    def __init__(self):
        super().__init__(GoalEntity)

    def create(self, data: Dict[str, Any]) -> GoalEntity:
        """
        Create a new GoalEntity with duplicate check for user_id + goal_date
        """
        # Check unique constraint: user_id + goal_date
        if "user_id" in data and "goal_date" in data:
            existing = self.check_duplicate({
                "user_id": data["user_id"],
                "goal_date": data["goal_date"]
            })
            if existing:
                raise CustomException(
                    exception=ExceptionType.DUPLICATE_ENTRY,
                    message=f"Goal for user {data['user_id']} on date {data['goal_date']} already exists"
                )
        
        return super().create(data)

