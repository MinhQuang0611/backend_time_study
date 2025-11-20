from fastapi_sqlalchemy import db
from app.models.model_session import SessionEntity, SessionPauseEntity
from app.services.srv_base import BaseService


class SessionService(BaseService[SessionEntity]):

    def __init__(self):
        super().__init__(SessionEntity)


class SessionPauseService(BaseService[SessionPauseEntity]):

    def __init__(self):
        super().__init__(SessionPauseEntity)

