# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  # noqa
from app.models.model_user import User  # noqa

# Room Database Entities
from app.models.model_user_entity import UserEntity  # noqa
from app.models.model_session import SessionEntity, SessionPauseEntity  # noqa
from app.models.model_task import TaskEntity, TaskSessionEntity  # noqa
from app.models.model_goal import GoalEntity  # noqa
from app.models.model_setting import UserSettingEntity, DefaultSettingEntity  # noqa
from app.models.model_statistics import StatisticsCacheEntity, StreakRecordEntity  # noqa
from app.models.model_shop import ShopEntity, ShopPurchaseEntity  # noqa
from app.models.model_external_account import ExternalAccount  # noqa
from app.models.model_facebook_friend import FacebookFriend  # noqa