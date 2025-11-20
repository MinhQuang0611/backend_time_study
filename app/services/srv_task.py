from fastapi_sqlalchemy import db
from app.models.model_task import TaskEntity, TaskSessionEntity
from app.services.srv_base import BaseService


class TaskService(BaseService[TaskEntity]):

    def __init__(self):
        super().__init__(TaskEntity)


class TaskSessionService(BaseService[TaskSessionEntity]):

    def __init__(self):
        super().__init__(TaskSessionEntity)

