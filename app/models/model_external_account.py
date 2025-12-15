from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from app.models.model_base import BareBaseModel

class ExternalAccount(BareBaseModel):
    __tablename__ = "external_accounts"

    external_account_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    provider = Column(String, nullable=False)
    provider_user_id = Column(String, nullable=False)

    name = Column(String)
    avatar_url = Column(String)

    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id"),
    )
